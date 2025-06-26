from fastapi import FastAPI, UploadFile, BackgroundTasks, Query, Response, Request, Depends
from redis import Redis

from alchemy import Session, User
from logic import StorageReader, StorageWriter, Archivator
from utils import PathValidEnsurer, Logger, PathJoiner, PathCutter, TimeHandler, Hasher
from depends import AuthDepend
from view_handlers import MakeDirHandler, FileResponseHandler, UploadFileHandler, StorageViewHandler, SignUpHandler, AuthHandler, LogOutHandler
from config import STORAGE_PATH, CACHE_EXPIRE_TIME, SESSION_EXPIRE_TIME, CACHE_PORT, CACHE_HOST
from schemas.query import UploadQuery, DownloadQuery, SignUpQuery, AuthenticateQuery, MakeDirInStorageQuery
from schemas.response import ViewStorageResponse
from cache_handler import RedisCacher
from db_repository import ModelReader, ModelActor
from auth import UserRegistration, UserAuthentication, SessionValidator, SessionMaker, UserGetter, SessionDeleter


app = FastAPI()
logger = Logger()
redis_client = Redis(host=CACHE_HOST, port=CACHE_PORT, decode_responses=True)
path_joiner = PathJoiner(STORAGE_PATH)
path_cutter = PathCutter(STORAGE_PATH)
path_ensurer = PathValidEnsurer(STORAGE_PATH, path_cutter, path_joiner)
archivator = Archivator()
time_handler = TimeHandler()
storage_reader = StorageReader(STORAGE_PATH, path_joiner, path_cutter)
storage_writer = StorageWriter(STORAGE_PATH)
hasher = Hasher()
redis_cacher = RedisCacher(redis_client, CACHE_EXPIRE_TIME)
user_reader = ModelReader(User, logger)
user_actor = ModelActor(User, logger)
session_reader = ModelReader(Session, logger)
session_actor = ModelActor(Session, logger)
session_validator = SessionValidator(time_handler)
session_maker = SessionMaker(int(SESSION_EXPIRE_TIME), session_actor, time_handler, hasher, redis_cacher)
user_getter = UserGetter(user_reader, session_reader, redis_cacher, session_validator)
user_registrator = UserRegistration(user_actor, hasher, logger)
user_authenticator = UserAuthentication(user_reader, session_maker, user_getter, logger, hasher)
session_deleter = SessionDeleter(redis_cacher, session_actor)
file_response_handler = FileResponseHandler(archivator, storage_reader, logger, path_ensurer, path_joiner)
upload_handler = UploadFileHandler(storage_writer, path_ensurer, logger, path_joiner)
storage_view_handler = StorageViewHandler(storage_reader, logger, path_joiner, path_cutter, path_ensurer)
sign_up_handler = SignUpHandler(user_registrator, storage_writer, user_reader)
auth_handler = AuthHandler(user_authenticator)
make_dir_handler = MakeDirHandler(logger, storage_writer, path_joiner, path_ensurer)
logout_handler = LogOutHandler(session_deleter, logger)

auth_depend = AuthDepend(auth_handler)



@app.get('/storage', response_model=ViewStorageResponse)
def view_storage_root(entity_path_in_storage = '', user=Depends(auth_depend.auth)):
    entities = storage_view_handler.get_list_of_entities(user.id, entity_path_in_storage)
    return {"entities": entities}


@app.get('/storage/{entity_path_in_storage:path}', response_model=ViewStorageResponse)
async def view_storage(entity_path_in_storage: str, user=Depends(auth_depend.auth)):
    entities = storage_view_handler.get_list_of_entities(user.id, entity_path_in_storage)
    return {"entities": entities}

@app.get('/download-entity')
def download_entity_endpoint(background_tasks: BackgroundTasks, params: DownloadQuery = Query(), user=Depends(auth_depend.auth)):
    response = file_response_handler.get_response(user.id, params.entity_path_in_storage)
    background_tasks.add_task(archivator.cleanup_temp_files)
    return response


@app.post('/upload-entity')
async def upload_entity_endpoint(files: list[UploadFile], params: UploadQuery = Query(), user=Depends(auth_depend.auth)):
    await upload_handler.save_files_to_storage(user.id, params.path_in_storage, files)
    return {"message": 'successfully uploaded files'}

@app.post('/make-dir-in-storage')
def make_dir_in_storage(user=Depends(auth_depend.auth), params: MakeDirInStorageQuery = Query()):
    make_dir_handler.make_dir_in_storage(user.id, params.path_in_storage, params.name)

@app.post('/log-out')
def log_out_endpoint(request: Request, response: Response):
    logout_handler.logout_user(request, response)


@app.post('/sign-up')
def sign_up_endpoint(params: SignUpQuery = Query()):
    sign_up_handler.sign_up(params)
    return {"message": 'successfully signed up'}

@app.post('/log-in')
def authenticate(response: Response, params: AuthenticateQuery = Query()):
    auth_handler.auth_with_psw_and_set_session_cookie(params.name, params.password, response)
    return {"message": 'successfully logged_in'}

