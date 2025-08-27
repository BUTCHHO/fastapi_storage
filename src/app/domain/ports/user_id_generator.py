from typing import Protocol
from uuid import UUID


class UserIdGenerator(Protocol):

    def generate_id(self) -> UUID: pass