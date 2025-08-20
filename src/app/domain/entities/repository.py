from dataclasses import dataclass
from uuid import UUID
from app.domain.enums.repository_statuses import RepositoryStatus


@dataclass
class Repository:
    id: UUID
    owners_id: list[UUID]
    limit_size: int
    files_count: int
    dirs_count: int
    current_size: int
    status: RepositoryStatus