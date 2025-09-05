from typing import Protocol

class Flusher(Protocol):
    async def flush(self) -> None:
        """
        :raises: DataMapperError, UserNameAlreadyExistsError
        """