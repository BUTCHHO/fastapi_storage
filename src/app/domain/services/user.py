from app.domain.value_objects.user.user_id import UserID
from app.domain.value_objects.user.user_name import UserName
from app.domain.value_objects.user.user_password_hash import UserPasswordHash
from app.domain.value_objects.user.raw_password import RawPassword

from app.domain.entities.user import User

from app.domain.enums.user_roles import UserRole

from app.domain.exceptions.user import UserRoleIsNotChangeable


class UserService:
    def __init__(self, user_id_generator, password_hasher):
        self._user_id_generator = user_id_generator
        self._password_hasher = password_hasher

    def create_user(
        self,
        username: UserName,
        raw_password: RawPassword,
        role: UserRole,
    ):
        user_id = UserID(self._user_id_generator())
        password_hash = UserPasswordHash(self._password_hasher.hash(raw_password))
        return User(
            id_=user_id,
            user_name=username,
            password_hash=password_hash,
            role=role,
        )

    def verify_password(self, user, raw_password):
        return self._password_hasher.verify(user.password_hash, raw_password)

    def change_username(self, user: User, new_name):
        user.user_name = UserName(new_name)

    def change_user_password(self, user: User, raw_password):
        user.password_hash = UserPasswordHash(self._password_hasher.hash(raw_password))

    def change_user_role(self, user, * ,is_admin:bool):
        if user.role.is_changeable:
            user.role = UserRole.ADMIN if is_admin else UserRole.USER
            return
        raise UserRoleIsNotChangeable()
