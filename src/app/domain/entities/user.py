from dataclasses import dataclass
from app.domain.enums.user_roles import UserRole
from app.domain.entities.base import Entity
from app.domain.value_objects.user.user_name import UserName
from app.domain.value_objects.user.user_password_hash import UserPasswordHash

@dataclass
class User(Entity):
    user_name: UserName
    password_hash: UserPasswordHash
    role: UserRole
    is_active: bool