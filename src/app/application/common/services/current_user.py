from app.application.common.ports.user_query_gateway import UserQueryGateway
from app.application.common.ports.identity_provider import IdentityProvider
from app.domain.entities.user import User
from app.domain.exceptions.user import UserDontExists, UserIsInactive


class CurrentUserService:

    def __init__(self,
                 identity_provider: IdentityProvider,
                 user_query_gateway: UserQueryGateway,

                 ):
        self._identity_provider = identity_provider
        self._user_query_gateway = user_query_gateway

    async def get_current_user(self) -> User:
        current_user_id = await self._identity_provider.get_current_user_id()
        current_user = await self._user_query_gateway.read_by_id(current_user_id)
        if current_user is None:
            raise UserDontExists
        if not current_user.is_active:
            raise UserIsInactive
        return current_user