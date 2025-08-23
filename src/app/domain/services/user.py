from app.domain.value_objects.user.user_id import UserID
from app.domain.value_objects.user.user_name import UserName
from app.domain.value_objects.user.user_password_hash import UserPasswordHash

from app.domain.entities.user import User

from app.domain.enums.user_roles import UserRole


class UserService:
    def __init__(self, user_id_generator, password_hash_generator):
        self._user_id_generator = user_id_generator
        self._password_hash_generator = password_hash_generator

    def create_user(
        self,
        username: UserName
        raw_pasword: Pa
    ):

    def change_username(self, user: User, new_name):
        User.user_name = UserName(new_name)

    def change_user_password(self, user: User, new_password):
        user.password_hash = UserPasswordHash(self._password_hash_generator(new_password))

    def change_user_role(self, user, * ,is_admin:bool):
        if user.role.is_changeable:
            user.role = UserRole.ADMIN if is_admin else UserRole.USER
            return
        raise UserRoleIsNotChagneable()