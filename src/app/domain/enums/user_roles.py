from enum import Enum



class UserRole(Enum):
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    USER = 'user'

    @property
    def is_changeable(self):
        return self != UserRole.SUPER_ADMIN

    @@property
    def is_assignable(self):
        return self != UserRole.SUPER_ADMIN
