from uuid import UUID
from dataclasses import dataclass
from app.domain.value_objects.base import ValueObject

@dataclass
class UserID(ValueObject):
    value: UUID
