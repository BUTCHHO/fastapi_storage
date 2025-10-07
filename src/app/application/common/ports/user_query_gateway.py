from typing import Protocol, List

from app.domain.entities.user import User
from app.domain.value_objects.user.user_id import UserID
from app.domain.value_objects.user.user_name.user_name import UserName

class UserQueryGateway(Protocol):
    async def read_by_id(self, user_id: UserID) -> User:
        """
        :raises: DataMapperError
        """

    async def read_by_name(self, name: UserName) -> User:
        """
        :raises: DataMapperError
        """

    async def read_all(self, limit:int, offset:int) -> List[User]:
        """
        :raises: DataMapperError
        """