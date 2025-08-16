from fastapi import HTTPException

class APIEntityIsNotADir(HTTPException):
    def __init__(self, path_in_storage):
        self.detail = {'message': f'entity at {path_in_storage} is not a directory', 'code':'entity_is_not_a_dir'}
        self.status_code = 400
        super().__init__(self.status_code, self.detail)

class APIPathGoesBeyondLimits(HTTPException):
    def __init__(self, path_in_storage):
        self.detail = {"message": f'path {path_in_storage} is goes beyond limits', "code": 'path_goes_beyond_limits'}
        self.status_code = 403
        super().__init__(status_code=self.status_code, detail=self.detail)

class APIEntityDoesNotExists(HTTPException):
    def __init__(self, path_in_storage):
        self.detail = {"message": f'entity at {path_in_storage} does not exists', "code": 'entity_does_not_exists'}
        self.status_code = 404
        super().__init__(status_code=self.status_code, detail=self.detail)

class APIUnsupportedEntityType(HTTPException):
    def __init__(self, entity_path_in_storage):
        self.detail = {"message":f'unsupported entity type {entity_path_in_storage}', "code":'unsupported_entity_type'}
        self.status_code = 415
        super().__init__(self.status_code, self.detail)

class APIUserStorageAlreadyExists(HTTPException):
    def __init__(self):
        self.status_code=409
        self.detail = {"message": 'Storage for this user already exists. Failed to create new storage', "code": 'user_storage_already_exists'}
        super().__init__(self.status_code, self.detail)

class APIDirectoryAlreadyExists(HTTPException):
    def __init__(self, path):
        self.status_code = 409
        self.detail = {"message": f'Directory at {path} already exists', "code":'diractory_already_exists'}
        super().__init__(self.status_code, self.detail)

