from typing import Protocol


class PasswordHasher(Protocol):

    def hash(self, raw_psw) -> bytes: pass

    def verify(self, raw_psw, hash_psw) -> bool: pass