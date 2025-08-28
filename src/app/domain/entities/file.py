from dataclasses import dataclass
from app.domain.entities.base import Entity
from app.domain.value_objects.file.filename.file_name import FileName
from app.domain.value_objects.file.fileformat.file_format import FileFormat
from app.domain.value_objects.file.file_hash import FileHash


@dataclass
class File(Entity):
    hash: FileHash
    format: FileFormat
    name: FileName
    size_bytes: int

