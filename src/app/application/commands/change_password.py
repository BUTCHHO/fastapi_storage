from dataclasses import dataclass
from logging import getLogger

from app.application.commands.base import Command
from app.application.common.ports.transaction_manager import TransactionManager
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.domain.exceptions.user import UserDontExists
from app.domain.services.user import UserService
from app.domain.value_objects.user.raw_password import RawPassword
from app.domain.value_objects.user.user_name.user_name import UserName

logger = getLogger(__name__)

@dataclass
class ChangePasswordQuery:
    username: UserName
    new_password: RawPassword

class ChangePasswordCommand(Command):
    def __init__(self,
                 user_service: UserService,
                 user_command_gateway: UserCommandGateway,
                 transaction_manager: TransactionManager,
                 ):
        self._user_service = user_service
        self._user_command_gateway = user_command_gateway
        self._transaction_manager = transaction_manager


    async def execute(self, request: ChangePasswordQuery):

        user = await self._user_command_gateway.read_by_username(request.username, for_update=True)

        if user is None:
            raise UserDontExists

        self._user_service.change_user_password(user, request.new_password)

        await self._transaction_manager.commit()