from typing import Protocol


class PasswordHasher(Protocol):

    def hash(self, raw_psw) -> bytes: ...

    def verify(self, raw_psw, hash_psw) -> bool: ...