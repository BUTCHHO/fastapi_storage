from dataclasses import dataclass

from app.application.commands.base import Command

from app.domain.entities.user import User
from app.domain.services.user import UserService
from app.domain.enums.user_roles import UserRole
from app.domain.value_objects.user.user_id import UserID
from app.domain.value_objects.user.user_name.user_name import UserName
from app.domain.value_objects.user.raw_password import RawPassword

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
                user_command_gateway
                ):
        self.user_service = user_service
        self.user_command_gateway = user_command_gateway

    async def execute(self, request_data: RequestData) -> UserCreateResponse:
        name = UserName(request_data.name)
        raw_password = RawPassword(request_data.raw_password)
        user = self.user_service.create_user(name, raw_password, request_data.role)
        return UserCreateResponse(user.id_)
