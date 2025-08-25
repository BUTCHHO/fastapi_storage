from app.domain.value_objects.base import ValueObject
from dataclasses import dataclass


@dataclass
class UserName(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()



