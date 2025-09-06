from typing import Protocol
from app.domain.value_objects.user.user_id import UserID

class IdentityProvider(Protocol):

    async def get_current_user_id(self) -> UserID: ...