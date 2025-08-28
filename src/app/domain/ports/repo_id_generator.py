from typing import Protocol
from uuid import UUID

class RepoIDGenerator():
    def generate(self) -> UUID: ...