from dataclasses import dataclass
from app.domain.value_objects.base import ValueObject


@dataclass
class RawPassword(ValueObject):
    value: str