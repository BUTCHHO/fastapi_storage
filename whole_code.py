from fastapi import FastAPI, UploadFile, BackgroundTasks, Query
from logic import StorageReader, StorageWriter, Archivator
from utils import PathValidEnsurer, Logger, PathJoiner
from view_handlers import FileResponseHandler, UploadFileHandler, StorageViewHandler
from config import STORAGE_PATH
from schemas.query import ViewStorageQuery, ViewStorageRootQuery, UploadQuery, DownloadQuery
app = FastAPI()
logger = Logger()
path_ensurer = PathValidEnsurer(STORAGE_PATH)
storage_reader = StorageReader(STORAGE_PATH)
storage_writer = StorageWriter(STORAGE_PATH)
path_joiner = PathJoiner(STORAGE_PATH)
archivator = Archivator()
file_response_handler = FileResponseHandler(archivator, storage_reader, logger, path_ensurer)
upload_handler = UploadFileHandler(storage_writer, path_ensurer, logger)
storage_view_handler = StorageViewHandler(storage_reader, logger, path_joiner)
@app.get('/storage')
def view_storage_root(params: ViewStorageRootQuery = Query()):
    abs_path = path_joiner.join_with_root_path(params.user_id)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, params.user_id)
    entities = storage_view_handler.get_list_of_entities(abs_path)
    return entities
@app.get('/storage/{path_in_storage:path}')
async def view_storage(params: ViewStorageQuery = Query()):
    abs_path = path_joiner.create_absolute_path(params.user_id, params.entity_path_in_storage)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, params.entity_path_in_storage)
    entities = storage_view_handler.get_list_of_entities(abs_path)
    return entities
@app.get('/download-entity')
def download_entity_endpoint(background_tasks: BackgroundTasks, params: DownloadQuery = Query()):
    abs_path = path_joiner.create_absolute_path(params.user_id, params.entity_path_in_storage)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, params.entity_path_in_storage)
    response = file_response_handler.get_response(abs_path, params.entity_path_in_storage)
    background_tasks.add_task(archivator.cleanup_temp_files)
    return response
@app.post('/upload-entity')
async def upload_entity_endpoint(files: list[UploadFile], params: UploadQuery = Query()):
    abs_path = path_joiner.create_absolute_path(params.user_id, params.path_in_storage)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, params.path_in_storage)
    await upload_handler.save_files_to_storage(abs_path, files)
from dotenv import load_dotenv
from os import getenv
from exceptions import StoragePathIsNone
load_dotenv('.env')
STORAGE_PATH = getenv('STORAGE_PATH')
if STORAGE_PATH is None:
    raise StoragePathIsNone
from fastapi.responses import FileResponse
from fastapi import HTTPException
from interfaces import IStorageReader, IArchivator, ILogger, IPathValidator
from exceptions import APIPathGoesBeyondLimits, APIEntityDoesNotExists, APIUnsupportedEntityType
from path_explorator import EntityDoesNotExists, PathGoesBeyondLimits
from utils import get_encoded_string
class FileResponseHandler:
    def __init__(self, archivator, storage_reader, logger, path_validator):
        self.archivator: IArchivator = archivator
        self.storage_reader: IStorageReader = storage_reader
        self.logger: ILogger = logger
        self.validator: IPathValidator = path_validator
        self.encode_string = get_encoded_string
    def _make_response(self, path_to_entity):
        try:
            str_path_to_entity = path_to_entity.__str__()
            entity_name = self.storage_reader.get_name(str_path_to_entity)
            encoded_entity_name = self.encode_string(entity_name)
            return FileResponse(path_to_entity,
                                filename=f'{entity_name}',
                                headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_entity_name}"},
    )
        except Exception as e:
            self.logger.log(e)
            raise e
    def get_zip_file_response(self, absolute_path_dir):
        try:
            zip_path = self.archivator.create_large_zip(absolute_path_dir)
            return self._make_response(zip_path)
        except Exception as e:
            self.logger.log(e)
    def get_file_response(self, absolute_path_file):
        return self._make_response(absolute_path_file)
    def ensure_path_valid_or_httpexception(self, absolute_path, entity_path_in_storage):
        try:
            self.validator.raise_if_path_invalid(absolute_path)
        except PathGoesBeyondLimits:
            raise APIPathGoesBeyondLimits(entity_path_in_storage)
        except EntityDoesNotExists:
            raise APIEntityDoesNotExists(entity_path_in_storage)
    def get_response(self, absolute_entity_path, entity_path_in_storage):
        self.ensure_path_valid_or_httpexception(absolute_entity_path, entity_path_in_storage)
        if self.storage_reader.is_dir(absolute_entity_path):
            return self.get_zip_file_response(absolute_entity_path)
        if self.storage_reader.is_file(absolute_entity_path):
            return self.get_file_response(absolute_entity_path)
        else:
            raise APIUnsupportedEntityType(entity_path_in_storage=entity_path_in_storage)
from interfaces import ILogger, IStorageReader, IPathJoiner
class StorageViewHandler:
    def __init__(self, storage_reader, logger, path_joiner):
        self.storage_reader: IStorageReader = storage_reader
        self.logger: ILogger = logger
        self.path_joiner: IPathJoiner = path_joiner
    def _get_abs_path(self, user_id, path_to_dir):
        path_with_user_id = self.path_joiner.join_paths(user_id, path_to_dir)
        return self.storage_reader.join_with_root_path(path_with_user_id)
    def _get_all_entitynames_in_dir(self, abs_dir_path):
        return self.storage_reader.get_all_entitynames_in_dir(abs_dir_path)
    def get_list_of_entities(self, abs_path):
        try:
            entitynames = self._get_all_entitynames_in_dir(abs_path)
            return entitynames
        except Exception as e:
            self.logger.log(e)from interfaces import IPathValidator, ILogger, IStorageWriter
class UploadFileHandler:
    def __init__(self, storage_writer, validator, logger):
        self.storage_writer: IStorageWriter = storage_writer
        self.validator: IPathValidator = validator
        self.logger: ILogger = logger
    def join_abs_fpath_and_fname(self, abs_path, fname):
        return f'{abs_path}/{fname}'
    async def _iterate_and_save_files_to_storage(self, files: list, output_path):
        try:
            for file in files:
                abs_file_path_and_name = self.join_abs_fpath_and_fname(output_path, file.filename)
                await self.storage_writer.async_write_from_fastapi_uploadfile_to_file(file, abs_file_path_and_name)
        except Exception as e:
            self.logger.log(e)
            raise e
    async def save_files_to_storage(self, absolute_path, files: list):
        await self._iterate_and_save_files_to_storage(files, absolute_path)
class Logger:
    @staticmethod
    def log(exception):
        print(f'LOG {exception}')
    @staticmethod
    def decor_log(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                Logger.log(e)
        return wrapper
from path_explorator import PathCreator
class PathJoiner(PathCreator):
    def __init__(self, root_path):
        self.root_path = root_path
        super().__init__()
    @property
    def root(self):
        return self.root_path
    def join_with_root_path(self, path:str | int):
        if isinstance(path, int):
            path = str(path)
        return self.join_paths(self.root_path, path)
    def create_absolute_path(self, user_id, entity_path_in_storage):
        user_id = str(user_id)
        path_in_storage_with_id = self.join_paths(user_id, entity_path_in_storage)
        return self.join_with_root_path(path_in_storage_with_id)from exceptions import APIPathGoesBeyondLimits
from path_explorator import PathGoesBeyondLimits, EntityDoesNotExists, PathValidator
class PathValidEnsurer(PathValidator):
    def __init__(self, storage_path):
        super().__init__(storage_path)
    def raise_if_goes_beyond_limits(self, requesting_path: str):
        if self.is_goes_beyond_limits(requesting_path):
            raise PathGoesBeyondLimits(requesting_path)
    def raise_if_entity_dont_exists(self, path:str):
        if not self.is_exists(path):
            raise EntityDoesNotExists(path)
    def raise_if_path_invalid(self, path:str):
        self.raise_if_goes_beyond_limits(path)
        self.raise_if_entity_dont_exists(path)
    def ensure_path_safety_on_endpoint_level(self, abs_path, path_in_storage):
        try:
            self.raise_if_goes_beyond_limits(abs_path)
        except PathGoesBeyondLimits:
            raise APIPathGoesBeyondLimits(path_in_storage)
from urllib.parse import quote
def get_encoded_string(string):
    return quote(string)
from pydantic import BaseModel, Field
class DownloadQuery(BaseModel):
    user_id: int = Field(ge=0)
    entity_path_in_storage: str
from pydantic import BaseModel, Field
class UploadQuery(BaseModel):
    user_id: int = Field(ge=0)
    path_in_storage: str
from pydantic import BaseModel, Field
class ViewStorageRootQuery(BaseModel):
    user_id: int = Field(ge=0)
class ViewStorageQuery(BaseModel):
    user_id: int = Field(ge=0)
    entity_path_in_storage: str
from pathlib import Path
from tempfile import mkdtemp
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
class Archivator:
    def create_large_zip(self, archived_dir: str) -> Path:
        archivable_dir = Path(archived_dir)
        temp_dir = Path(mkdtemp())
        self.zip_path = temp_dir / f"{archivable_dir.name}.zip"
        try:
            with ZipFile(
                    self.zip_path,
                    mode='w',
                    compression=ZIP_DEFLATED,
                    allowZip64=True,
                    compresslevel=6
            ) as zipf:
                for file_path in archivable_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(archivable_dir)
                        zipf.write(file_path, arcname)
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise e
        return self.zip_path
    def cleanup_temp_files(self):
        temp_dir = self.zip_path.parent
        try:
            self.zip_path.unlink(missing_ok=True)
            temp_dir.rmdir()
        except OSError:
            shutil.rmtree(temp_dir, ignore_errors=True)from path_explorator import DirectoryExplorer
class StorageReader(DirectoryExplorer):
    def __init__(self, root_dir):
        super().__init__(root_dir)
from path_explorator import DirectoryActor
class StorageWriter(DirectoryActor):
    def __init__(self, root_dir):
        super().__init__(root_dir)from typing import Callable
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
    def decor_log(self, func) -> Callable: passclass StoragePathIsNone(Exception):
    def __init__(self):
        msg = 'STORAGE_PATH value from .env file is None. Must be filled'
        super().__init__(msg)from fastapi import HTTPException
class APIPathGoesBeyondLimits(HTTPException):
    def __init__(self, path_in_storage, detail=None, status_code=403):
        if not detail:
            detail = {"message": f'path {path_in_storage} is goes beyond limits', "code": 'path_goes_beyond_limits'}
        super().__init__(status_code=status_code, detail=detail)
class APIEntityDoesNotExists(HTTPException):
    def __init__(self, path_in_storage, detail=None, status_code=404):
        if not detail:
            detail = {"message": f'entity at {path_in_storage} does not exists', "code": 'entity_does_not_exists'}
        super().__init__(status_code=status_code, detail=detail)
class APIUnsupportedEntityType(HTTPException):
    def __init__(self, entity_path_in_storage, detail=None, status_code=415):
        if not detail:
            detail = {"message":f'unsupported entity type {entity_path_in_storage}', "code":'unsupported_entity_type'}
        super().__init__(status_code, detail)