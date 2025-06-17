from fastapi import FastAPI, UploadFile, BackgroundTasks, Query

from alchemy import Session, User
from logic import StorageReader, StorageWriter, Archivator
from utils import PathValidEnsurer, Logger, PathJoiner, PathCutter, TimeHandler, Hasher
from view_handlers import FileResponseHandler, UploadFileHandler, StorageViewHandler, SignUpHandler
from config import STORAGE_PATH
from schemas.query import ViewStorageQuery, ViewStorageRootQuery, UploadQuery, DownloadQuery, SignUpQuery, LogInQuery
from schemas.response import ViewStorageResponse

from db_repository import ModelReader, ModelActor

from auth import UserRegistration

#TODO refactor alchemy package, refactor db_repository

app = FastAPI()
logger = Logger()
path_ensurer = PathValidEnsurer(STORAGE_PATH)
storage_reader = StorageReader(STORAGE_PATH)
storage_writer = StorageWriter(STORAGE_PATH)
path_joiner = PathJoiner(STORAGE_PATH)
path_cutter = PathCutter()
archivator = Archivator()
hasher = Hasher()

user_reader = ModelReader(User, logger)
user_actor = ModelActor(User, logger)
session_reader = ModelReader(Session, logger)
session_actor = ModelActor(Session, logger)

user_registrator = UserRegistration(user_reader, user_actor, hasher, logger)

file_response_handler = FileResponseHandler(archivator, storage_reader, logger, path_ensurer)
upload_handler = UploadFileHandler(storage_writer, path_ensurer, logger)
storage_view_handler = StorageViewHandler(storage_reader, logger, path_joiner, path_cutter)
sign_up_handler = SignUpHandler(user_registrator)

@app.post('/sign-up')
def sign_up_endpoint(params: SignUpQuery = Query()):
    sign_up_handler.sign_up(params)

@app.post('/log-in')
def log_in(params: LogInQuery = Query()):
    #TODO auth system

    return {'message': 'not implemented endpoint'}



@app.get('/storage', response_model=ViewStorageResponse)
def view_storage_root(params: ViewStorageRootQuery = Query()):
    abs_path = path_joiner.join_with_root_path(params.user_id)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, params.user_id)
    entities = storage_view_handler.get_list_of_entities(abs_path)
    return {"entities": entities}


@app.get('/storage/{entity_path_in_storage:path}', response_model=ViewStorageResponse)
async def view_storage(entity_path_in_storage: str, params: ViewStorageQuery = Query()):
    abs_path = path_joiner.create_absolute_path(params.user_id, entity_path_in_storage)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, entity_path_in_storage)
    entities = storage_view_handler.get_list_of_entities(abs_path)
    return {"entities": entities}

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


