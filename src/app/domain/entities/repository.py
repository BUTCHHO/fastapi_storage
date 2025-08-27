from dataclasses import dataclass

from app.domain.enums.repository_statuses import RepositoryStatus
from app.domain.entities.base import Entity
from app.domain.value_objects.repository.repository_id import RepositoryID
from app.domain.value_objects.repository.name.repository_name import RepositoryName
from app.domain.value_objects.repository.limit.limit_size import RepositoryLimitSize


@dataclass
class Repository(Entity):
    id: RepositoryID
    name: RepositoryName
    limit_size: RepositoryLimitSize
    files_count: int
    dirs_count: int
    current_size: int
    status: RepositoryStatus