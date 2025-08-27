from app.domain.value_objects.base import ValueObject
from app.domain.value_objects.repository.name.validation import validate_name_pattern, validate_name_length
from dataclasses import dataclass


@dataclass()
class RepositoryName(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()
        validate_name_length(self.value)
        validate_name_pattern(self.value)
