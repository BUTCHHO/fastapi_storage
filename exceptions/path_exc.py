from fastapi import HTTPException

class APIPathGoesBeyondLimits(HTTPException):
    def __init__(self, path_in_storage, detail=None, status_code=403):
        if not detail:
            detail = {"message": f'path {path_in_storage} is goes beyond limits', "code": 'path_goes_beyond_limits'}
        super().__init__(status_code=status_code, detail=detail)

class APIEntityDoesNotExists(HTTPException):
    def __init__(self, path_in_storage, detail=None, status_code=404):
        if not detail:
            detail = {"message": f'entity at {path_in_storage} does not exists', "code": 'entity_does_not_exists'}
        super().__init__(status_code=status_code, detail=detail)