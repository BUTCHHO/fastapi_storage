from dataclasses import dataclass

from logging import getLogger

from app.application.commands.base import Command
from app.application.common.ports.flusher import Flusher
from app.application.common.ports.transaction_manager import TransactionManager

from app.domain.services.user import UserService
from app.domain.enums.user_roles import UserRole
from app.domain.value_objects.user.user_id import UserID
from app.domain.value_objects.user.user_name.user_name import UserName
from app.domain.value_objects.user.raw_password import RawPassword
from app.domain.exceptions.user import UserNameAlreadyExists

from app.application.common.ports.user_command_gateway import UserCommandGateway

logger = getLogger(__name__)

@dataclass
class RequestData:
    name: str
    raw_password: str
    role: UserRole

@dataclass
class UserCreateResponse:
    id: UserID

class UserCreateCommand(Command):
    def __init__(self,
                user_service: UserService,
                user_command_gateway: UserCommandGateway,
                flusher: Flusher,
                transaction_manager: TransactionManager,
                ):
        self._user_service = user_service
        self._user_command_gateway = user_command_gateway
        self._flusher = flusher
        self._transaction_manager = transaction_manager

    async def execute(self, request_data: RequestData) -> UserCreateResponse:
        name = UserName(request_data.name)
        raw_password = RawPassword(request_data.raw_password)
        user = self._user_service.create_user(name, raw_password, request_data.role)
        self._user_command_gateway.add(user)

        try:
            await self._flusher.flush()
        except UserNameAlreadyExists:
            logger.error(f'User {name} already exists')

        await self._transaction_manager.commit()

        return UserCreateResponse(user.id_)
