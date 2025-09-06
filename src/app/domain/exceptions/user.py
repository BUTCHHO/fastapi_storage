from app.domain.exceptions.base import DomainError


class UserRoleIsNotChangeable(DomainError):
    def __init__(self):
        msg = 'User role change is not permitted'
        super().__init__(msg)

class UserNameAlreadyExists(DomainError):
    def __init__(self):
        msg = "User Name already exists"
        super().__init__(msg)

class UserDontExists(DomainError):
    def __init__(self):
        msg = "User dont exists"
        super().__init__(msg)

class UserIsInactive(DomainError):
    def __init__(self):
        msg = "user is inactive"
        super().__init__(msg)