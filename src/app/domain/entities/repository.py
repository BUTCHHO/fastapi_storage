from dataclasses import dataclass
from app.domain.enums.repository_statuses import RepositoryStatus
from app.domain.entities.base import Entity
from app.domain.value_objects.repository.repository_id import RepositoryID
from app.domain.value_objects.user.user_id import UserID

@dataclass
class Repository(Entity):
    id: RepositoryID
    owners_id: list[UserID]
    limit_size: int
    files_count: int
    dirs_count: int
    current_size: int
    status: RepositoryStatus