from dataclasses import dataclass


@dataclass
class User():
    user_name: str
    password_hash: str
    role: UserRole
    is_active: bool