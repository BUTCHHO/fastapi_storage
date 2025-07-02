from redis import Redis

from auth.user_deleter import UserDeleter
from utils import Logger, TimeHandler, PathCutter, PathJoiner, PathValidEnsurer, Hasher
from logic import StorageReader, StorageWriter, Archivator, StorageDeleter
from db_repository import ModelReader, ModelActor
from auth import UserRegistration, UserLogout, UserAuthentication ,SessionValidator, SessionMaker, SessionDeleter, UserGetter
from cache_handler import RedisCacher
from alchemy import User, Session

from config import STORAGE_PATH, CACHE_EXPIRE_TIME, CACHE_HOST, CACHE_PORT, SESSION_EXPIRE_TIME

logger = Logger()
redis_client = Redis(host=CACHE_HOST, port=CACHE_PORT, decode_responses=True)
path_joiner = PathJoiner(STORAGE_PATH)
path_cutter = PathCutter(STORAGE_PATH)
path_ensurer = PathValidEnsurer(STORAGE_PATH, path_cutter, path_joiner)
archivator = Archivator()
time_handler = TimeHandler()
storage_reader = StorageReader(STORAGE_PATH, path_joiner, path_cutter)
storage_writer = StorageWriter(STORAGE_PATH)
storage_deleter = StorageDeleter(storage_writer)
hasher = Hasher()
redis_cacher = RedisCacher(redis_client, CACHE_EXPIRE_TIME)
user_reader = ModelReader(User, logger)
user_actor = ModelActor(User, logger)
session_reader = ModelReader(Session, logger)
session_actor = ModelActor(Session, logger)
session_deleter = SessionDeleter(redis_cacher, session_actor, session_reader)
session_validator = SessionValidator(time_handler, session_deleter)
session_maker = SessionMaker(int(SESSION_EXPIRE_TIME), session_actor, time_handler, hasher, redis_cacher)
user_getter = UserGetter(user_reader, session_reader, redis_cacher, session_validator)
user_registrator = UserRegistration(user_actor, hasher, logger)
user_authenticator = UserAuthentication(user_reader, session_maker, user_getter, logger, hasher)
user_logouter = UserLogout(session_deleter)
user_deleter = UserDeleter(user_actor)