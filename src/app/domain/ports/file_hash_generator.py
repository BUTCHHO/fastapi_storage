from typing import Protocol
from io import IOBase


class FileHashGenerator(Protocol):

    def generate(self, file_obj: IOBase) -> str: ...
