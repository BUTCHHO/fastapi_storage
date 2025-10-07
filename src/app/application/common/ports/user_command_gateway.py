from typing import Protocol

from app.domain.entities.user import User
from app.domain.value_objects.user.user_name.user_name import UserName


class UserCommandGateway(Protocol):
    def add(self, user: User) -> None:
        """
        :raises: DataMapperError
        """

    async def read_by_username(self, username: UserName, for_update:bool=False) -> User:
        """
        :raises: DataMapperError
        """

    async def delete_user_by_username(self, username: UserName) -> None:
        """
        :raises: DataMapperError
        :raises: UserDontExistError
        """