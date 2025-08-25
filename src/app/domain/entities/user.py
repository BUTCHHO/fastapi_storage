from dataclasses import dataclass, field
from typing import Dict

from app.domain.value_objects.user.user_id import UserID


from app.domain.enums.user_roles import UserRole, UserRepositoryRole
from app.domain.entities.base import Entity
from app.domain.value_objects.user.user_name.user_name import UserName
from app.domain.value_objects.repository.repository_id import RepositoryID
from app.domain.value_objects.user.user_password_hash import UserPasswordHash

@dataclass
class User(Entity):
    id_: UserID
    user_name: UserName
    password_hash: UserPasswordHash
    user_role: UserRole
    repositories_roles: Dict[RepositoryID, UserRepositoryRole] = field(default_factory=dict)
