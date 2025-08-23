class UserRoleIsNotChangeable(Exception):
    def __init__(self):
        msg = 'User role change is not permitted'
        super().__init__(msg)