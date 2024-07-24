from typing import Any, get_type_hints
from copy import deepcopy
from threading import Lock
import inspect
from functools import wraps

from kisa_utils.response import Response, Ok, Error
from kisa_utils.structures.validator import validateWithResponse
from kisa_utils.structures.validator import Value
from kisa_utils import dates
from kisa_utils.db import Handle
from kisa_utils.encryption import decrypt, encrypt
from kisa_utils.storage import encodeJSON, decodeJSON

from . import __config__

def __saveState(method):
    def decorated(instance, *args, **kwargs):
        if (response := method(instance, *args, **kwargs)):
            instance._Permissions__autoSave()
        return response

    return decorated

class Permissions:

    __dbTableName = 'permissions'
    __dbTables = {
        __dbTableName: '''
            creationTimestamp varchar(25) not null,
            details text not null
        ''',
    }

    # locks used to update properties during write operations
    __locks = {'__global__': Lock()}

    # this dictionary will enable our class to be a singleton. only one object/instance should be used for a single projectId
    __uniqueInstances = {}

    @property 
    def version(self,) -> str:
        return '1.0'

    @property
    def id(self) -> str:
        return self.__id

    @property
    def globalPermissions(self) -> str:
        return [permission for permission in self.__globalPermissions]

    @property
    def resources(self) -> str:
        return {resource: [permission for permission in self.__resources[resource]] for resource in self.__resources}

    @property
    def users(self) -> str:
        return deepcopy(self.__users)

    # make this class a singleton
    def __new__(cls, *args, **kwargs) -> 'Permissions':
        projectId = args[0]
        with Permissions.__locks['__global__']:
            if projectId in Permissions.__uniqueInstances:
                return Permissions.__uniqueInstances[projectId]

        instance = super().__new__(cls)
        Permissions.__uniqueInstances[projectId] = instance
        return instance

    def __init__(self, projectId:str, /, *, dbPath:str=__config__.paths['db']):

        if not (response := self.__projectIdValidator(projectId)).status:
            raise ValueError(response.log)

        if not __config__.Path.createDirectory(dbPath)['status']:
            raise ValueError(f'failed to creaet permissions path: {dbPath}')
        
        self.__dbFilePath = f'{dbPath}/{__config__.dbFileName.format(projectId=projectId)}'

        self.__id = projectId
        self.__globalPermissions = {}
        self.__resources = {}
        self.__users = {}
        self.__lastModified = '1970-01-01 00:00:00'

        with Permissions.__locks['__global__']:
            if self.__id not in Permissions.__locks:
                Permissions.__locks[self.__id] = Lock()

        if not (response:=self.__loadFromDatabase()) and response.log!='no-saved-data':
            import sys
            sys.exit(f'[PANIC] error loading permissions: {response.log}')

    # utils...
    def __autoSave(self) -> Response:
        # print('xxx')
        self.__lastModified = dates.currentTimestamp()
        data = encrypt(encodeJSON(self.export()), password=self.__id)
        with Handle(self.__dbFilePath, tables=Permissions.__dbTables, readonly=False, useWALMode=True) as handle:
            if not (response := handle.insert(self.__dbTableName, [
                dates.currentTimestamp(),
                data
            ])):
                print(f'permissions save error: {response["log"]}')
                Error(response['log'])

        return Ok()
    
    def __loadFromDatabase(self) -> Response:
        with Handle(self.__dbFilePath, tables=Permissions.__dbTables, readonly=True) as handle:
            data = handle.fetch(Permissions.__dbTableName, ['details'],'1 order by rowid desc',[], limit=1)
            if not data:
                return Error('no-saved-data')

            data = data[0][0]

            try:
                data = decrypt(data, password=self.__id)
            except:
                return Error('failed to decrypt saved permissions')

            try:
                data = decodeJSON(data)
            except:
                return Error('failed to parsed decrypted saved permissions')


            self.__id = data['id']
            self.__resources = data['resources']
            self.__users = data['users']
            self.__lastModified = data['lastModified']

            return Ok()

    @globals()['__saveState']
    def __setUserPermission(self, user:str, resource:str, permission:str, status:bool) -> Response:
        if user not in self.__users:
            return Error('user not registered in permissions')

        if resource not in self.__resources:
            return Error('resource not registered in permissions')

        if resource not in self.__users[user]:
            return Error('user not subscribed to resource')

        if (permission not in self.__resources[resource]) and (permission not in self.__globalPermissions):
            return Error('permission not registered in the resource or global permissions')
        
        with Permissions.__locks[self.__id]:
            self.__users[user][resource][permission] = status

        return Ok()

    # accessors and settors...
    @globals()['__saveState']
    def addGlobalPermissions(self, permissions:list[str]) -> Response:
        if not (response := self.__permissionsListValidator(permissions)):
            return response

        with Permissions.__locks[self.__id]:
            for permission in permissions:
                if permission not in self.__globalPermissions:
                    self.__globalPermissions[permission] = None

        return Ok()

    @globals()['__saveState']
    def deleteGlobalPermissions(self, permissions:str|list[str]) -> Response:
        if not isinstance(permissions, list):
            permissions = [permissions]

        with Permissions.__locks[self.__id]:
            # verification loop
            for permission in permissions:
                if permission not in self.__globalPermissions:
                    return Error(f'permission `{permission}` is not a global permission')
                
            # action loop
            for permission in permissions:
                del(self.__globalPermissions[permission])

        return Ok()

    def load(self, exportedData:dict) -> Response:
        pass

    def export(self) -> dict:
        return {
            'version': self.version,
            'id': self.__id,
            'lastModified': self.__lastModified,
            'globalPermissions':deepcopy(self.__globalPermissions),
            'resources': deepcopy(self.__resources),
            'users': deepcopy(self.__users),
        }

    @globals()['__saveState']
    def addResources(self, resources:dict[str, list[str]]) -> Response:
        '''
        attempt to add resources to the permissions instance
        @param `resources:dict[str, list[str]]`: the resources `dict` in format
            {
                resource1:str : [permission1:str, permission2:str,...],
                resource2:str : [permission1:str, permission2:str,...],

                ...
            }
        '''
        if not (response := validateWithResponse(resources,Value(dict, self.__resourceDictValidator))):
            return response

        with Permissions.__locks[self.__id]:
            for resource in resources:
                if resource in self.__resources:
                    return Error(f'resource `{resource}` already present')

                # self.__resources[resource] = {permission:resources[resource].index(permission) for permission in resources[resource]}
                self.__resources[resource] = {permission:None for permission in resources[resource]}

        return Ok()

    @globals()['__saveState']
    def addUsers(self, users:dict[str, dict[str, dict[str, bool]]]) -> Response:
        '''
        attempt to add users to the permissions instance
        @param `users:dict[str, dict[str, dict[str, bool]]]`: the resources `dict` in format
            {
                user1:str : {
                    resource1:str : {
                        permission1:str : bool,
                        permission2:str : bool,

                        ...
                    },

                    ...
                },

                ...
            }
        '''
        if not (response := validateWithResponse(users,Value(dict, self.__usersDictValidator))):
            return response

        with Permissions.__locks[self.__id]:
            for user in users:
                self.__users[user] = deepcopy(users[user])

        return Ok()

    @globals()['__saveState']
    def deleteUser(self, user:str) -> Response:
        if user not in self.__users:
            return Error('user not found in permissions')

        with Permissions.__locks[self.__id]:
            del(self.__users[user])

        return Ok()

    def permissionIsActivated(self, *, user:str='', resource:str='', permission:str='') -> Response:
        if user not in self.__users:
            return Error('user not registered in permissions')

        if resource not in self.__resources:
            return Error('resource not registered in permissions')

        if resource not in self.__users[user]:
            return Error('user not subscribed to resource')

        if (permission not in self.__resources[resource]) and (permission not in self.__globalPermissions):
            return Error('permission not registered in the resource or global permissions')

        return Ok() if self.__users[user][resource].get(permission,False) else Error('permission not activated for the user')

    @globals()['__saveState']
    def addUserPermission(self, user:str, resource:str, permission:str, *, status:bool = True) -> Response:
        if user not in self.__users:
            return Error('user not registered in permissions')

        if resource not in self.__resources:
            return Error('resource not registered in permissions')

        if resource not in self.__users[user]:
            return Error('user not subscribed to resource')

        if (permission not in self.__resources[resource]) and (permission not in self.__globalPermissions):
            return Error('permission not registered in the resource or global permissions')

        if permission in self.__users[user][resource]:
            return Error('permission already registered to the user')

        with Permissions.__locks[self.__id]:
            self.__users[user][resource][permission] = status

        return Ok()

    @globals()['__saveState']
    def deleteUserPermission(self, user:str, resource:str, permission:str) -> Response:
        if user not in self.__users:
            return Error('user not registered in permissions')

        if resource not in self.__resources:
            return Error('resource not registered in permissions')

        if resource not in self.__users[user]:
            return Error('user not subscribed to resource')

        if permission not in self.__resources[resource]:
            return Error('permission not registered in the resource')

        if permission not in self.__users[user][resource]:
            return Error('permission not registered to the user')

        with Permissions.__locks[self.__id]:
            del(self.__users[user][resource][permission])

        return Ok()

    @globals()['__saveState']
    def activateUserPermission(self, user:str, resource:str, permission:str) -> Response:
        return self.__setUserPermission(user, resource, permission, True)

    @globals()['__saveState']
    def deactivateUserPermission(self, *, user:str, resource:str, permission:str) -> Response:
        return self.__setUserPermission(user, resource, permission, False)

    @globals()['__saveState']
    def deleteResource(self, resource:str) -> Response:
        with Permissions.__locks[self.__id]:
            if resource not in self.__resources:
                return Error('resource not in permissions instance')
            del(self.__resources[resource])

        return Ok()

    @globals()['__saveState']
    def addResourcePermissions(self, resource:str, permissions:str | list[str]) -> Response:
        if not isinstance(permissions, list):
            permissions = [permissions]

        if not (response := self.__permissionsListValidator(permissions)):
            return response

        with Permissions.__locks[self.__id]:
            if resource not in self.__resources:
                return Error('resource not in permissions instance')
            for permission in permissions:
                self.__resources[resource][permission] = None

        return Ok()

    @globals()['__saveState']
    def deleteResourcePermissions(self, resource:str, permissions:list[str]) -> Response:
        if not (response := self.__permissionsListValidator(permissions)):
            return response

        with Permissions.__locks[self.__id]:
            if resource not in self.__resources:
                return Error('resource not in permissions instance')

            for permission in permissions:
                del(self.__resources[resource][permission])

        return Ok()

    def resourceHasPermission(self, resource:str, permission:str) -> Response:
        if resource not in self.__resources:
            return Error('resource not in permissions instance')

        return Ok() if permission in self.__resources[resource] else Error('resource has no permission')

    # validators...
    def __projectIdValidator(self, projectId:str) -> Response:
        if not ((' ' not in projectId) and len(projectId) and (not projectId.startswith('__'))):
            return Error('invalid id given. expected non-zero-length string with no spaces and not starting with `__`')

        for sequence in ['..','/']:
            if sequence in projectId:
                return Error(f'`{sequence}` not allowed in the id')

        return Ok()

    def __permissionValidator(self, permission:str) -> Response:
        if not (isinstance(permission,str) and (' ' not in permission) and len(permission)):
            return Error('invalid permission, expected string with no spaces')

        return Ok()

    def __permissionsListValidator(self, permissions:list[str]) -> Response:
        _permissions = list(set(permissions))
        if len(permissions) != len(_permissions):
            return Error('resource contains duplicate permissions')

        if not permissions:
            return Error('no permissions provided')

        permissions = _permissions

        for index, permission in enumerate(permissions):
            if not (rep := self.__permissionValidator(permission)):
                return Error(f'permission at index #{index}(`{permission}`), error:{rep.log}')

            if permission in self.__globalPermissions:
                return Error(f'permission at index #{index}(`{permission}`), error:global permission can not be added to resource')

        return Ok()

    def __resourceDictValidator(self, resources:dict[str, str|list[str]]) -> Response:
        for resource in resources:

            if not (isinstance(resource,str) and (' ' not in resource) and len(resource)):
                return Error(f'invalid resource name given(`{resource}`), expected string with no spaces')

            permissions = resources[resource]
            if not isinstance(permissions,list):
                return Error(f'invalid permissions given for resource `{resource}`, expected list[str]')

            if not (rep := self.__permissionsListValidator(permissions)):
                return Error(f'resource `{resource}` error:{rep.log}')

        return Ok()

    def __usersDictValidator(self, users:dict[str, dict[str, dict[str, bool]]]) -> Response:
        for user in users:

            if not (isinstance(user,str) and (' ' not in user) and len(user)):
                return Error(f'invalid user given(`{user}`), expected string with no spaces')

            if user in self.__users:
                return Error(f'user `{user}` already registered')

            resources = users[user]
            if not isinstance(resources,dict):
                return Error(f'invalid resources given for user `{user}`, expected dict[str, dict[str, bool]]')

            for resource in resources:
                if not (isinstance(resource,str) and (' ' not in resource) and len(resource)):
                    return Error(f'invalid resource given(`{user}->{resource}`), expected string with no spaces')

                if resource not in self.__resources:
                    return Error(f'resource `{user}->{resource}` not yet registered')

                permissions = resources[resource]
                if not isinstance(permissions,dict):
                    return Error(f'invalid permission given(`{user}->{resource}->{permissions}`), expected dict[str,bool]')

                for permission in permissions:
                    if not (response:=self.__permissionValidator(permission)):
                        return Error(f'invalid permission given(`{user}->{resource}->{permission}`), error:{response.log}')

                    if not isinstance(permissions[permission], bool):
                        return Error(f'invalid permission value given(`{user}->{resource}->{permission}`), expected bool')

                    if permission not in self.__resources[resource]:
                        return Error(f'permission `{user}->{resource}->{permission}` not defined in resource `{resource}`')


        return Ok()

# authentication decorators...

def __decoratedFunctionReturnsKISAResponse(func) -> Response:
    funcName = func.__name__
    returnTypeErrorFound = False
    try:
        # prefer typing.get_type_hints to the inbuild `__annotations__` attribute
        # if func.__annotations__['return'] != Response:
        if get_type_hints(func)['return'] != Response:
            returnTypeErrorFound = True
    except:
        returnTypeErrorFound = True

    if returnTypeErrorFound:
        return Error(f'[authenticator:{funcName}]: decorated function MUST return a KISA-Response object only in its signature')

    return Ok()

def __extractSingleAuthenticatorData(func, _user:str, _resource:str, *funcArgs, **funcKwargs) -> Response:
    data = {
        'user':None,
        'resource':None,
    }

    signatureParameters = list(inspect.signature(func).parameters)

    for index, parameterName in enumerate(signatureParameters):
        if index >= len(funcArgs): break

        if parameterName==_user:
            data['user'] = funcArgs[index]
            continue
        elif parameterName==_resource:
            data['resource'] = funcArgs[index]
            continue

    if not (None!=data['user'] and None!=data['resource']):
        for kwarg in funcKwargs:
            if kwarg==_user:
                data['user'] = funcKwargs[kwarg]
                continue
            elif kwarg==_resource:
                data['resource'] = funcKwargs[kwarg]
                continue

    return Ok(data) if (None!=data['user'] and None!=data['resource']) else Error('[verifyPermissions]: could not find both the specified `user` and `resource` in the decorated function')

def verifyPermissions(perm:Permissions,/,*,user:str, resource:str, permissions:str|list[str], checkAll:bool=True):
    '''
    authorize permission

    @param `perm:Permissions`: the Permissions instance to use for authentication
    @param `user:str`: the user to authorize using the `perm` instance. The value passed should be the name of an argument or keyword argument that identifies a user in the decorated function
    @param `resource:str`: the resource to authorize using the `perm` instance. The value passed should be the name of an argument or keyword argument that identifies a resource in the decorated function
    @param `permissions:str|list[str]`: a single permission or list of permissions to authorize
    @param `checkAll:bool`: if `True` then ALL permissions must pass the verification test, otherwise verification will be successful if ANY permission passes the test

    @retrurn: `kisa_utils.response.Response`
    '''

    if not isinstance(permissions, list):
        permissions = [permissions]

    def decorator(func):
        funcName = func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(perm, Permissions):
                return Error(f'[authenticator:{funcName}]: first decorator argument should be an isntance of `Permissions`')
            
            if not permissions:
                return Error(f'[authenticator:{funcName}]: no permissions registered at function decoration')

            if not (response := __decoratedFunctionReturnsKISAResponse(func)):
                return response

            if not (response:=__extractSingleAuthenticatorData(func, user, resource, *args, **kwargs)):
                return response

            runtimeUser, runtimeResource = response.data['user'], response.data['resource']

            checks = [
                perm.permissionIsActivated(user=runtimeUser, resource=runtimeResource, permission=permission)
                for permission in permissions
            ]

            if checkAll and not all(checks):
                return [response for response in checks if not response][0]
            else:
                if not any(checks):
                    return checks[0]

            response = func(*args, **kwargs)
            if not isinstance(response, Response):
                return Error(f'[authenticator:{funcName}]: decorated function did not return a KISA-Response object')
            return response

        return wrapper

    return decorator
