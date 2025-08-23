from dataclasses import dataclass
from app.domain.value_objects.base import ValueObject

@dataclass
class UserPasswordHash(ValueObject):
    value: bytes