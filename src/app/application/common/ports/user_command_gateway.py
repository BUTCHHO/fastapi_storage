from typing import Protocol

from app.domain.entities.user import User
from app.domain.value_objects.user.user_name.user_name import UserName


class UserCommandGateway(Protocol):
    def add(self, user: User) -> None:
        """
        :raises: DataMapperError
        """

    def read_by_username(self, username: UserName, for_update:bool=False) -> User:
        """
        :raises: DataMapperError
        """
