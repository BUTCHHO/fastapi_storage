from typing import Protocol, List

from app.domain.entities.user import User
from app.domain.value_objects.user.user_id import UserID
from app.domain.value_objects.user.user_name.user_name import UserName

class UserQueryGateway(Protocol):
    def read_by_id(self, user_id: int) -> User:
        """
        :raises: DataMapperError
        """

    def read_by_name(self, name: UserName) -> User:
        """
        :raises: DataMapperError
        """

    def read_all(self) -> List[User]:
        """
        :raises: DataMapperError
        """