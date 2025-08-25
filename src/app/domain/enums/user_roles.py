from enum import Enum



class UserRole(Enum):
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    USER = 'user'

    @property
    def is_changeable(self):
        return self != UserRole.SUPER_ADMIN

    @property
    def is_assignable(self):
        return self != UserRole.SUPER_ADMIN

class UserRepositoryRole(Enum):
    OWNER = 2 #can read/add files, delete repository, add contributors and readers, change repo status etc
    CONTRIBUTOR = 1 #can read/add files
    READER = 0 #can read files
