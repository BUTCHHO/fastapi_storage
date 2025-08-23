from dataclasses import dataclass
from uuid import UUID

from app.domain.value_objects.base import ValueObject


@dataclass
class RepositoryID(ValueObject):
    value: UUID