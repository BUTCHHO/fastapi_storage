class UserAlreadyExists(Exception):
    def __init__(self, name):
        msg = f'User with name {name} already exists'
        super().__init__(msg)

class Unauthorized(Exception):
    def __init__(self, name = None):
        msg = f'user {name} unauthorized'
        super().__init__(msg)

class UserDontExists(Exception):
    def __init__(self, name=None):
        msg = f'User with name {name} does not exists'
        super().__init__(msg)

class IncorrectPassword(Exception):
    def __init__(self):
        super().__init__()

class SessionExpired(Exception):
    def __init__(self):
        super().__init__()

class SessionDontExists(Exception):
    def __init__(self):
        super().__init__()