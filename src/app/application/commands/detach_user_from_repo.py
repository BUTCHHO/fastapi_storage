from dataclasses import dataclass
from logging import getLogger

from app.application.commands.base import Command
from app.application.commands.create_user import UserCreateResponse
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.application.common.ports.transaction_manager import TransactionManager
from app.domain.exceptions.user import UserRepositoryRoleIsNotChangeable, UserRoleIsNotDetachable
from app.domain.services.user import UserService
from app.domain.value_objects.repository.repository_id import RepositoryID
from app.domain.value_objects.user.user_name.user_name import UserName


logger = getLogger(__name__)

@dataclass
class DetachUserFromRepoQuery:
    repo_id: RepositoryID
    username: UserName


class DetachUserFromRepoCommand(Command):
    def __init__(self,
                 user_command_gateway: UserCommandGateway,
                 user_service: UserService,
                 transaction_manager: TransactionManager,
                 ):
        self._user_command_gateway = user_command_gateway
        self._user_service = user_service
        self._transaction_manager = transaction_manager

    async def execute(self, request: DetachUserFromRepoQuery):
        user = await self._user_command_gateway.read_by_username(username=request.username, for_update=True)

        try:
            self._user_service.detach_user_from_repo(user, repository_id=request.repo_id)
        except UserRoleIsNotDetachable:
            logger.info('user repository role is not detachable')
            raise

        await self._transaction_manager.commit()