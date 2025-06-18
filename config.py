from dotenv import load_dotenv
from os import getenv
from exceptions import StoragePathIsNone, DatabaseUrlIsNone, MemCachePortIsNone, MemCacheExpireTimeIsNone, MemCacheHostIsNone, SessionMakerKeyIsNone

load_dotenv('.env')

STORAGE_PATH = getenv('STORAGE_PATH')
DATABASE_URL = getenv('DATABASE_URL')
SESSION_EXPIRE_TIME = getenv('SESSION_EXPIRE_TIME')
SESSION_COOKIES_EXPIRE_TIME = getenv('SESSION_COOKIES_EXPIRE_TIME')
SESSION_MAKER_KEY = getenv('SESSION_MAKER_KEY')
MEMCACHE_HOST = getenv('MEMCACHE_HOST')
MEMCACHE_PORT = getenv('MEMCACHE_PORT')
MEMCACHE_EXPIRE_TIME = getenv('MEMCACHE_VALUE_EXPIRE_TIME')


if STORAGE_PATH is None:
    raise StoragePathIsNone
if DATABASE_URL is None:
    raise DatabaseUrlIsNone
if SESSION_MAKER_KEY is None:
    raise SessionMakerKeyIsNone
if MEMCACHE_HOST is None:
    raise MemCacheHostIsNone
if MEMCACHE_PORT is None:
    raise MemCachePortIsNone
if MEMCACHE_EXPIRE_TIME is None:
    raise MemCacheExpireTimeIsNone
