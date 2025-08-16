from fastapi.exceptions import HTTPException


class APIUserAlreadyExists(HTTPException):
    def __init__(self):
        self.detail = {"message": f'User with this name already exists', "code": 'user_already_exists'}
        self.status_code = 409
        super().__init__(self.status_code, self.detail)

class APIUserDontExists(HTTPException):
    def __init__(self, name=None):
        self.detail = {"message": f'User with name {name} dont exists', "code": 'user_dont_exists'}
        self.status_code = 404
        super().__init__(self.status_code, self.detail)

class APIIncorrectPassword(HTTPException):
    def __init__(self):
        self.detail = {"message": f'Incorrect password', "code": 'incorrect_password'}
        self.status_code = 401
        super().__init__(self.status_code, self.detail)

class APISessionDontExists(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = {"message": f'Session dont exists', "code": 'session_dont_exists'}
        super().__init__(self.status_code, self.detail)

class APISessionExpired(HTTPException):
    def __init__(self):
        self.detail = {"message": f'Session expired', "code": 'session_expired'}
        self.status_code = 440
        super().__init__(self.status_code, self.detail)

class APIUnauthorized(HTTPException):
    def __init__(self):
        self.detail = {"message": f'you have to log in to see this page', "code": 'unauthorized'}
        self.status_code = 401
        super().__init__(self.status_code, self.detail)