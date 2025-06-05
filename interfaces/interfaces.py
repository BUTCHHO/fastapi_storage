from typing import Callable
from abc import ABC, abstractmethod
from path_explorator import DirectoryExplorer

class IStorageReader(ABC):
    @abstractmethod
    def get_name(self,path:str) -> str: pass
    @abstractmethod
    def is_dir(self, path:str) -> bool: pass
    @abstractmethod
    def is_file(self, path:str) -> bool: pass
    @abstractmethod
    def join_with_root_path(self, path:str) -> str: pass
    @abstractmethod
    def get_all_entitynames_in_dir(self, path: str) -> list[str]: pass

class IStorageWriter(ABC):
    @abstractmethod
    async def async_write_from_fastapi_uploadfile_to_file(self, source_file, output_file_path:str) -> None: pass

class IArchivator(ABC):
    @abstractmethod
    def create_large_zip(self, path: str) -> str: pass

class IPathValidator(ABC):
    @abstractmethod
    def raise_if_path_invalid(self, path:str) -> None: pass
    @abstractmethod
    def raise_if_goes_beyond_limits(self, path:str) -> None: pass
    @abstractmethod
    def is_goes_beyond_limits(self, path:str) -> bool: pass
    @abstractmethod
    def is_exists(self, path:str) -> bool: pass

class IPathJoiner(ABC):
    @abstractmethod
    def join_paths(self, path1: str, path2: str) -> str: pass

class ILogger(ABC):
    @abstractmethod
    def log(self, exception) -> None: pass
    @abstractmethod
    def decor_log(self, func) -> Callable: pass