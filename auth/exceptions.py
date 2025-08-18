class UserAlreadyExists(Exception):
    def __init__(self, name=''):
        self.detail = f'User {name} already exists'
        super().__init__(self.detail)

class UserDontExists(Exception):
    def __init__(self):
        self.detail = f'User dont exists'
        super().__init__(self.detail)

class IncorrectPassword(Exception):
    def __init__(self, password=None):
        self.detail = f'Wrong password'
        super().__init__(self.detail)

class UserAlreadyHaveSession(Exception):
    def __init__(self, user_id=None):
        self.detail = f'User {user_id} already have session'
        super().__init__(self.detail)

class SessionDontExists(Exception):
    def __init__(self, user_id=None):
        msg = f'Session for user {user_id} dont exists'
        super().__init__(msg)

class SessionExpired(Exception):
    def __init__(self, ses_id=None):
        msg = f'Session {ses_id} dont exists'
        super().__init__(msg)

class Unauthorized(Exception):
    def __init__(self):
        msg = f'Unauthorized'
        super().__init__(msg)