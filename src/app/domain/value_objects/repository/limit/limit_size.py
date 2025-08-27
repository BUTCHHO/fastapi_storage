from app.domain.value_objects.repository.limit.validation import validate_limit_size
from app.domain.value_objects.base import ValueObject

from dataclasses import dataclass


@dataclass
class RepositoryLimitSize(ValueObject):
    value: int

    def __post_init__(self):
        super().__post_init__()
        validate_limit_size(self.value)