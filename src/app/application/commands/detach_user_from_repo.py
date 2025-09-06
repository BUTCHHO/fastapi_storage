from dataclasses import dataclass
from logging import getLogger

from app.application.commands.base import Command
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.application.common.ports.transaction_manager import TransactionManager
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