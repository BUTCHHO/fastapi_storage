from dotenv import load_dotenv
from os import getenv
from exceptions import StoragePathIsNone, DatabaseUrlIsNone, SessionMakerKeyIsNone, CachePortIsNone, CacheHostIsNone, CacheExpireTimeIsNone

load_dotenv('.env')

STORAGE_PATH = getenv('STORAGE_PATH')
DATABASE_URL = getenv('DATABASE_URL')
SESSION_EXPIRE_TIME = getenv('SESSION_EXPIRE_TIME')
SESSION_COOKIES_EXPIRE_TIME = getenv('SESSION_COOKIES_EXPIRE_TIME')
SESSION_MAKER_KEY = getenv('SESSION_MAKER_KEY')
CACHE_HOST = getenv('CACHE_HOST')
CACHE_PORT = int(getenv('CACHE_PORT'))
CACHE_EXPIRE_TIME = getenv('CACHE_EXPIRE_TIME')


if STORAGE_PATH is None:
    raise StoragePathIsNone
if DATABASE_URL is None:
    raise DatabaseUrlIsNone
if SESSION_MAKER_KEY is None:
    raise SessionMakerKeyIsNone
if CACHE_HOST is None:
    raise CacheHostIsNone
if CACHE_PORT is None:
    raise CachePortIsNone
if CACHE_EXPIRE_TIME is None:
    raise CacheExpireTimeIsNone
