from dataclasses import dataclass

from app.domain.value_objects.user.user_name.validation import validate_name_pattern, validate_username_length
from app.domain.value_objects.base import ValueObject


@dataclass
class UserName(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()
        validate_username_length(self.value)
        validate_name_pattern(self.value)



