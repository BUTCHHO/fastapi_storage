from redis import Redis

# from auth.user_deleter import UserDeleter not impl
from utils import Logger, TimeHandler, PathCutter, PathJoiner, PathValidEnsurer, Hasher
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
user_reader = ModelReader(User, logger, async_engine)
user_actor = ModelActor(User, logger, async_engine)
session_reader = ModelReader(Session, logger, async_engine)
session_actor = ModelActor(Session, logger, async_engine)
session_maker = SessionMaker(session_reader, session_actor, time_handler, hasher, redis_cacher, int(SESSION_EXPIRE_TIME))
user_getter = UserGetter(user_reader, session_reader, redis_cacher, time_handler)
user_registrator = Registrator(user_actor, user_reader, hasher)
user_authenticator = Authenticator(user_getter, hasher, session_maker, session_reader, redis_cacher)
user_logouter = Logouter(user_reader, session_reader, session_actor, redis_cacher)
# user_deleter = UserDeleter(user_actor) not impl