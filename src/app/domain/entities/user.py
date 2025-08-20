from dataclasses import dataclass
from app.domain.enums.user_roles import UserRole

@dataclass
class User():
    user_name: str
    password_hash: str
    role: UserRole
    is_active: bool