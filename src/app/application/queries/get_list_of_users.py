from dataclasses import dataclass
from logging import getLogger
from typing import List

from app.application.common.ports.user_query_gateway import UserQueryGateway
from app.domain.entities.user import User

logger = getLogger(__name__)

@dataclass
class GetListOfUsersQuery:
    limit: int
    offset: int

@dataclass
class GetListOfUsersResponse:
    users: List[User]

class GetListOfUsersQueryGateway:
    def __init__(self,
                 user_query_gateway: UserQueryGateway,):

        self._user_query_gateway = user_query_gateway

    async def execute(self, request: GetListOfUsersQuery):
        try:
            users = await self._user_query_gateway.read_all(request.limit, request.offset)
        except Exception as e:
            logger.error(f'Failed to get users from {request.limit} to {request.offset}: {e}')
            raise from e
        return GetListOfUsersResponse(users)