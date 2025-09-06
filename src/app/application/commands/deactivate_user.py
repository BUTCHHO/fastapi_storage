from dataclasses import dataclass
from logging import getLogger

from app.application.commands.base import Command
from app.application.common.ports.transaction_manager import TransactionManager
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.domain.exceptions.base import DomainError
from app.domain.exceptions.user import UserDontExists, UserActivationIsNotPermitted
from app.domain.services.user import UserService
from app.domain.value_objects.user.user_name.user_name import UserName

logger = getLogger(__name__)

@dataclass
class DeactivateUserQuery:
    user_name: UserName

class DeactivateUserCommand(Command):
    def __init__(self,
                 user_service: UserService,
                 transaction_manager: TransactionManager,
                 user_command_gateway: UserCommandGateway
                 ):
        self._user_service = user_service
        self._transaction_manager = transaction_manager
        self._user_command_gateway = user_command_gateway

    async def execute(self, request: DeactivateUserQuery):

        user = await self._user_command_gateway.read_by_username(request.user_name, for_update=True)

        if user is None:
            raise UserDontExists
        try:
            self._user_service.toggle_user_activation(user, is_active=False)
        except UserActivationIsNotPermitted:
            logger.info('user deactivation is not permitted')
            raise
        await self._transaction_manager.commit()
