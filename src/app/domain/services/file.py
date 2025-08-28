from app.domain.entities.file import File

from app.domain.value_objects.file.file_hash import FileHash
from app.domain.value_objects.file.filename.file_name import FileName
from app.domain.value_objects.file.fileformat.file_format import FileFormat

from app.domain.ports.file_hash_generator import FileHashGenerator

from io import IOBase



class FileService:
    def __init__(self, file_hash_generator):
        self._file_hash_generator: FileHashGenerator = file_hash_generator

    def create_file(self, file_obj:IOBase, file_format: FileFormat, name: FileName, size_bytes: int):
        file_hash = FileHash(self._file_hash_generator.generate(file_obj))
        return File(hash=file_hash,
                    format=file_format,
                    name=name,
                    size_bytes=size_bytes)

    def rename_file(self, file: File, new_name: FileName):
        file.name = new_name


