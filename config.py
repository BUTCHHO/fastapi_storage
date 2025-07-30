from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')

class Config:
    STORAGE_PATH = getenv('STORAGE_PATH')
    TEST_STORAGE_PATH = getenv('GET_TEST_STORAGE')
    DATABASE_URL = getenv('DATABASE_URL')
    TEST_DATABASE_URL = getenv('TEST_DATABASE_URL')
    SESSION_EXPIRE_TIME = getenv('SESSION_EXPIRE_TIME_DAYS')
    SESSION_COOKIES_EXPIRE_TIME = getenv('SESSION_COOKIES_EXPIRE_TIME_SECONDS')
    CACHE_HOST = getenv('CACHE_HOST')
    CACHE_PORT = int(getenv('CACHE_PORT'))
    CACHE_EXPIRE_TIME = getenv('CACHE_EXPIRE_TIME_SECONDS')


    assert STORAGE_PATH is not None
    assert TEST_STORAGE_PATH is not None
    assert TEST_DATABASE_URL is not None
    assert DATABASE_URL is not None
    assert SESSION_EXPIRE_TIME is not None
    assert SESSION_COOKIES_EXPIRE_TIME is not None
    assert CACHE_PORT is not None
    assert CACHE_HOST is not None
    assert CACHE_EXPIRE_TIME is not None

