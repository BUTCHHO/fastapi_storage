from fastapi.exceptions import HTTPException


class APIUserAlreadyExists(HTTPException):
    def __init__(self, name, detail=None, status_code=409):
        if not detail:
            detail = {"message": f'User with name {name} already exists', "code": 'user_already_exists'}
        super().__init__(status_code, detail)

class APIUserDontExists(HTTPException):
    def __init__(self, name, detail=None, status_code = 404):
        if not detail:
            detail = {"message": f'User with name {name} dont exists', "code": 'user_dont_exists'}
        super().__init__(status_code, detail)

class APIIncorrectPassword(HTTPException):
    def __init__(self, detail=None, status_code=401):
        if not detail:
            detail = {"message": f'Incorrect password', "code": 'incorrect_password'}
        super().__init__(status_code, detail)

class APISessionDontExists(HTTPException):
    def __init__(self, detail=None, status_code=404):
        if not detail:
            detail = {"message": f'Session dont exists', "code": 'session_dont_exists'}
        super().__init__(status_code, detail)

class APISessionExpired(HTTPException):
    def __init__(self):
        detail = {"message": f'Session expired', "code": 'session_expired'}
        status_code = 440
        super().__init__(status_code, detail)

class APIUnauthorized(HTTPException):
    def __init__(self):
        detail = {"message": f'you have to log in to see this page', "code": 'unauthorized'}
        status_code = 401
        super().__init__(status_code, detail)