from app.domain.value_objects.base import ValueObject

from app.domain.value_objects.file.fileformat.validation import validate_file_format

from dataclasses import dataclass



@dataclass
class FileFormat(ValueObject):
    value: str


    def __post_init__(self):
        super().__post_init__()
        validate_file_format(self.value)