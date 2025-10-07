from dataclasses import dataclass
from logging import getLogger

from app.application.commands.base import Command
from app.application.common.ports.transaction_manager import TransactionManager
from app.application.common.ports.flusher import Flusher
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.domain.exceptions.user import UserDontExists
from app.domain.services.user import UserService
from app.domain.value_objects.user.user_name.user_name import UserName

logger = getLogger(__name__)

@dataclass
class DeleteUserCommandQuery:
    user_name: UserName

class DeleteUserCommand(Command):
    def __init__(self,
                 transaction_manager: TransactionManager,
                 flusher: Flusher,
                 user_service: UserService,
                 user_command_gateway: UserCommandGateway) -> None:
        self._transaction_manager = transaction_manager
        self._flusher = flusher
        self._user_command_gateway = user_command_gateway
        self._user_service = user_service

    async def execute(self, request: DeleteUserCommandQuery):
        try:
            await self._user_command_gateway.delete_user_by_username(request.user_name)
        except Exception as e:
            logger.error(f"Failed to delete user {request.user_name} due to: {e}")

        try:
            await self._flusher.flush()
        except UserDontExists:
            logger.info(f"{request.user_name} dont exists")

        await self._transaction_manager.commit()
