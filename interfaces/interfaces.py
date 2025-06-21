from typing import Callable
from abc import ABC, abstractmethod

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
    @abstractmethod
    def create_dir(self, path: str, name: str, exist_ok=True): pass
    @abstractmethod
    def create_file(self, path: str, name: str, exist_ok=True): pass

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

class IPathCutter(ABC):
    @abstractmethod
    def cut_user_id_from_storage_path(self, path) -> str: pass
    @abstractmethod
    def get_user_id_part(self, path)-> str: pass

class IModelReader(ABC):
    @abstractmethod
    def get_by_id(self, id: int): pass
    @abstractmethod
    def get_by_kwargs(self, **kwargs): pass
    @abstractmethod
    def does_record_with_kwargs_exists(self, **kwargs) -> bool: pass


class IModelActor(ABC):
    @abstractmethod
    def create_and_write_record_to_db(self, **kwargs): pass
    @abstractmethod
    def create_record(self, **kwargs): pass
    @abstractmethod
    def write_record_to_db(self, record): pass
    @abstractmethod
    def delete_record_by_kwargs(self, **kwargs): pass
    @abstractmethod
    def delete_record_by_id(self, id): pass

class ITimeHandler(ABC):
    @abstractmethod
    def is_date_future(self, date) -> bool: pass
    @abstractmethod
    def add_days_to_current_date(self, days) -> object: pass
    @abstractmethod
    def get_today_date(self) -> object: pass
    @abstractmethod
    def get_str_today_date(self) -> str: pass