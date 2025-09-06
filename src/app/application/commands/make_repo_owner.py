from dataclasses import dataclass
from logging import getLogger

from app.application.commands.base import Command
from app.application.common.ports.transaction_manager import TransactionManager
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.domain.exceptions.user import UserNameAlreadyExists, UserRepositoryRoleIsNotChangeable
from app.domain.services.user import UserService
from app.domain.value_objects.repository.repository_id import RepositoryID
from app.domain.value_objects.user.user_name.user_name import UserName
from app.domain.enums.user_roles import UserRepositoryRole

logger = getLogger(__name__)

@dataclass
class MakeRepoOwnerQuery:
    repo_id: RepositoryID
    username: UserName

class MakeRepoOwnerCommand(Command):
    def __init__(self,
                 user_command_gateway: UserCommandGateway,
                 user_service: UserService,
                 transaction_manager: TransactionManager,
                 ):
        self._user_command_gateway = user_command_gateway
        self._user_service = user_service
        self._transaction_manager = transaction_manager

    async def execute(self, request: MakeRepoOwnerQuery):
        user = await self._user_command_gateway.read_by_username(request.username, for_update=True)

        if user is None:
            raise UserNameAlreadyExists()

        try:
            self._user_service.attach_repo_role_to_user(user, request.repo_id, UserRepositoryRole.OWNER)
        except UserRepositoryRoleIsNotChangeable:
            logger.info('user is already owner, passing exception')

        await self._transaction_manager.commit()
