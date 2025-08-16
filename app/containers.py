from dependency_injector import containers, providers
from redis import Redis
from utils import TimeHandler, PathCutter, PathJoiner, PathValidEnsurer, Hasher
from logic import StorageReader, StorageWriter, Archivator, StorageDeleter
from db_repository import ModelReader, ModelActor
from auth.registration import Registrator
from auth.authentication import Authenticator
from auth.logouter import Logouter
from auth.session_maker import SessionMaker
from auth.user_getter import UserGetter
from cache_handler import RedisCacher
from alchemy import User, Session
from alchemy.async_engine import async_engine

from app.routes.storage_acting.endpoint_handlers import MakeDirHandler, DeleteEntityHandler
from app.routes.upload.endpoint_handlers import UploadFileHandler
from app.routes.settings.endpoint_handlers import SettingsHandler
from app.routes.authorization.endpoint_handlers import SignUpHandler, LogOutHandler, AuthHandler
from app.routes.browser.handlers import BrowserEndpointHandler
from app.routes.download.endpoint_handlers import FileResponseHandler

from depends.auth import AuthDepend

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    async_engine_provider = providers.Object(async_engine)

    redis_client = providers.Singleton(Redis, host=config.CACHE_HOST, port=config.CACHE_PORT, decode_responses=True)
    path_joiner = providers.Singleton(PathJoiner, config.STORAGE_PATH)
    path_cutter = providers.Singleton(PathCutter, config.STORAGE_PATH)
    path_ensurer = providers.Singleton(PathValidEnsurer, config.STORAGE_PATH, path_cutter, path_joiner)
    archivator = providers.Singleton(Archivator)
    time_handler = providers.Singleton(TimeHandler)
    storage_reader = providers.Singleton(StorageReader, config.STORAGE_PATH, path_joiner, path_cutter)
    storage_writer = providers.Singleton(StorageWriter, config.STORAGE_PATH)
    storage_deleter = providers.Singleton(StorageDeleter, storage_writer)
    hasher = providers.Singleton(Hasher)
    cacher = providers.Singleton(RedisCacher, redis_client, config.CACHE_EXPIRE_TIME)
    user_reader = providers.Singleton(ModelReader, User, async_engine_provider)
    user_actor = providers.Singleton(ModelActor, User, async_engine_provider)
    session_reader = providers.Singleton(ModelReader, Session, async_engine_provider)
    session_actor = providers.Singleton(ModelActor, Session, async_engine_provider)
    session_maker = providers.Singleton(SessionMaker, session_reader, session_actor, time_handler, hasher, cacher, config.SESSION_EXPIRE_TIME)
    user_getter = providers.Singleton(UserGetter, user_reader, session_reader, session_actor, cacher, time_handler)
    user_registrator = providers.Singleton(Registrator, user_actor, user_reader, hasher)
    user_authenticator = providers.Singleton(Authenticator, user_getter, hasher, session_maker, session_reader, cacher)
    user_logouter = providers.Singleton(Logouter, user_reader, session_reader, session_actor, cacher)



    make_dir_handler = providers.Singleton(MakeDirHandler, storage_writer, path_joiner, path_ensurer)
    delete_entity_handler = providers.Singleton(DeleteEntityHandler, path_ensurer, storage_writer, path_joiner)
    upload_file_handler = providers.Singleton(UploadFileHandler, storage_writer, path_ensurer, path_joiner)
    settings_handler = providers.Singleton(SettingsHandler, user_actor, user_logouter, storage_deleter)
    sign_up_handler = providers.Singleton(SignUpHandler, user_registrator, storage_writer, user_reader, user_actor, hasher, config.STORAGE_ID_LEN)
    logout_handler = providers.Singleton(LogOutHandler, user_logouter)
    auth_handler = providers.Singleton(AuthHandler, user_authenticator, config.SESSION_COOKIES_EXPIRE_TIME)
    browser_endpoint_handler = providers.Singleton(BrowserEndpointHandler, storage_reader, path_joiner, path_cutter, path_ensurer)
    file_response_handler = providers.Singleton(FileResponseHandler, archivator, storage_reader, path_ensurer, path_joiner)


    auth_depend = providers.Singleton(AuthDepend, auth_handler)
    auth_provider = providers.Callable(auth_depend().auth)
    ask_for_password_provider = providers.Callable(auth_depend().ask_for_password)