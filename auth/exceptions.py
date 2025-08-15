class UserAlreadyExists(Exception):
    def __init__(self, name=''):
        msg = f'User {name} already exists'
        super().__init__(msg)

class UserDontExists(Exception):
    def __init__(self, id=None):
        msg = f'User with id {id} dont exists'
        super().__init__(msg)

class IncorrectPassword(Exception):
    def __init__(self, password=None):
        msg = f'Wrong password {password}'
        super().__init__(msg)

class UserAlreadyHaveSession(Exception):
    def __init__(self, user_id=None):
        msg = f'User {user_id} already have session'
        super().__init__(msg)

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