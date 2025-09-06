from dataclasses import dataclass
from logging import getLogger

from app.application.commands.create_user import UserCreateResponse
from app.application.common.ports.flusher import Flusher
from app.application.common.ports.transaction_manager import TransactionManager
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.domain.exceptions.base import DomainError
from app.domain.exceptions.user import UserDontExists
from app.domain.services.user import UserService
from app.domain.value_objects.user.user_id import UserID
from app.domain.value_objects.user.user_name.user_name import UserName

from app.application.commands.base import Command

logger = getLogger(__name__)

@dataclass
class ActivateUserQuery:
    user_name: UserName



class ActivateUserCommand(Command):
    def __init__(self,
                 user_command_gateway: UserCommandGateway,
                 flusher: Flusher,
                 transaction_manager: TransactionManager,
                 user_service: UserService
                 ):
        self._user_command_gateway = user_command_gateway
        self._flusher = flusher
        self._transaction_manager = transaction_manager
        self._user_service = user_service

    def execute(self, username: UserName) -> UserCreateResponse:
        user = self._user_command_gateway.read_by_username(username, for_update=True)

        if user is None:
            logger.info(f"User {username} not found")
            raise UserDontExists

        try:
            self._user_service.activate_user(user)
        except DomainError:
            logger.info(f"User {username} is already active")
            raise

        self._transaction_manager.commit()

