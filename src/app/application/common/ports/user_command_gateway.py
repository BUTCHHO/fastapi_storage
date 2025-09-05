from typing import Protocol

from app.domain.entities.user import User

class UserCommandGateway(Protocol):
    def add(self, user: User) -> None:
        """
        :raises: DataMapperError
        """