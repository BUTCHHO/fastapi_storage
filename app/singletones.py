from redis import Redis

from auth.user_deleter import UserDeleter
from utils import Logger, TimeHandler, PathCutter, PathJoiner, PathValidEnsurer, Hasher
from logic import StorageReader, StorageWriter, Archivator, StorageDeleter
from db_repository import ModelReader, ModelActor
from auth import UserRegistration, SessionGetter, UserLogout, UserAuthentication ,SessionValidator, SessionMaker, SessionDeleter, UserGetter
from cache_handler import RedisCacher
from alchemy import User, Session
from alchemy.async_engine import async_engine

from config import STORAGE_PATH, CACHE_EXPIRE_TIME, SESSION_EXPIRE_TIME

logger = None
path_joiner = None
path_cutter = None
path_ensurer = None 
archivator = None 
time_handler = None
storage_reader = None
storage_writer = None
storage_deleter = None
hasher = None
redis_cacher = None
user_reader = None
user_actor = None
session_reader = None
session_actor = None
session_deleter = None 
session_validator =  None
session_maker = None
session_getter = None
user_getter = None
user_registrator = None
user_authenticator = None
user_logouter = None
user_deleter = None

def init_parameter_requiring_singletons(storage_path, redis_client):
    global logger
    global path_joiner
    global path_cutter
    global path_ensurer
    global archivator
    global time_handler
    global storage_reader
    global storage_writer
    global storage_deleter
    global hasher
    global redis_cacher
    global user_reader
    global user_actor
    global session_reader
    global session_actor
    global session_deleter
    global session_validator
    global session_maker
    global session_getter
    global user_getter
    global user_registrator
    global user_authenticator
    global user_logouter
    global user_deleter

    logger = Logger()
    path_joiner = PathJoiner(storage_path)
    path_cutter = PathCutter(storage_path)
    path_ensurer = PathValidEnsurer(storage_path, path_cutter, path_joiner)
    archivator = Archivator()
    time_handler = TimeHandler()
    storage_reader = StorageReader(storage_path, path_joiner, path_cutter)
    storage_writer = StorageWriter(storage_path)
    storage_deleter = StorageDeleter(storage_writer)
    hasher = Hasher()
    redis_cacher = RedisCacher(redis_client, CACHE_EXPIRE_TIME)
    user_reader = ModelReader(User, logger, async_engine)
    user_actor = ModelActor(User, logger, async_engine)
    session_reader = ModelReader(Session, logger, async_engine)
    session_actor = ModelActor(Session, logger, async_engine)
    session_deleter = SessionDeleter(redis_cacher, session_actor, session_reader)
    session_validator = SessionValidator(time_handler, session_deleter)
    session_maker = SessionMaker(int(SESSION_EXPIRE_TIME), session_actor, time_handler, hasher, redis_cacher)
    session_getter = SessionGetter(session_reader, redis_cacher, session_validator, session_deleter)
    user_getter = UserGetter(user_reader, session_reader, redis_cacher, session_validator)
    user_registrator = UserRegistration(user_actor, hasher, logger)
    user_authenticator = UserAuthentication(user_reader, session_getter, session_maker, user_getter, logger, hasher)
    user_logouter = UserLogout(session_deleter)
    user_deleter = UserDeleter(user_actor)