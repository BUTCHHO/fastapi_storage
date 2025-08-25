from app.domain.value_objects.repository.repository_id import RepositoryID
from app.domain.value_objects.user.user_id import UserID
from app.domain.value_objects.user.user_name.user_name import UserName
from app.domain.value_objects.user.user_password_hash import UserPasswordHash
from app.domain.value_objects.user.raw_password import RawPassword

from app.domain.exceptions.base import DomainError

from app.domain.entities.user import User
from app.domain.entities.repository import Repository

from app.domain.enums.user_roles import UserRole, UserRepositoryRole
from app.domain.enums.repository_statuses import RepositoryStatus

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
            user_role=role,
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

    def attach_repo_role_to_user(self, user: User, repo_id:RepositoryID, user_repo_roles:type(UserRepositoryRole.READER)):
        """gives ability to user to interact with repo"""
        user.repositories_roles[repo_id] = user_repo_roles

    def detach_user_from_repo(self, user: User, repository_id:RepositoryID):
        """removes from user ability to interact with repo"""
        if repository_id not in user.repositories_roles.keys():
            raise DomainError(f"User{user.id_} is not attached to repository {repository_id}")
        user.repositories_roles.pop(repository_id)

    def is_able_to_read_repo(self, user: User, repo: Repository):
        if repo.status == RepositoryStatus.PUBLIC:
            return True
        if repo.id in user.repositories_roles.keys():
            return True
        return False

    def is_able_to_contribute_repo(self, user: User, repo: Repository):
        if repo.id not in user.repositories_roles.keys():
            return False
        if user.repositories_roles[repo.id] > UserRepositoryRole.READER:
            return True
        return False