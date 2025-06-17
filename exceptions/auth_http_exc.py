from fastapi.exceptions import HTTPException


class APIUserAlreadyExists(HTTPException):
    def __init__(self, name, detail=None, status_code=409):
        if not detail:
            detail = {"message": f'User with name {name} already exists', "code": 'user_already_exists'}
        super().__init__(status_code, detail)