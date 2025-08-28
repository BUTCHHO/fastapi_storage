from app.domain.value_objects.base import ValueObject

from app.domain.value_objects.file.filename.validation import validate_filename_length, validate_filename_pattern

from dataclasses import dataclass



@dataclass
class FileName(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()
        validate_filename_length(self.value)
        validate_filename_pattern(self.value)