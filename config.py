from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')


class Config:
    STORAGE_PATH = getenv('STORAGE_PATH')
    STORAGE_ID_LEN = int(getenv('STORAGE_ID_LEN'))
    DATABASE_URL = getenv('DATABASE_URL')
    SESSION_EXPIRE_TIME = int(getenv('SESSION_EXPIRE_TIME_DAYS'))
    SESSION_COOKIES_EXPIRE_TIME = getenv('SESSION_COOKIES_EXPIRE_TIME_SECONDS')
    CACHE_HOST = getenv('CACHE_HOST')
    CACHE_PORT = int(getenv('CACHE_PORT'))
    CACHE_EXPIRE_TIME = getenv('CACHE_EXPIRE_TIME_SECONDS')
    ZIPS_PATH = getenv('ZIPS_PATH')

    @classmethod
    def to_dict(cls):
        config = {'STORAGE_PATH':cls.STORAGE_PATH,
                  'STORAGE_ID_LEN': cls.STORAGE_ID_LEN,
                  'DATABASE_URL': cls.DATABASE_URL,
                  'SESSION_EXPIRE_TIME': cls.SESSION_EXPIRE_TIME,
                  'SESSION_COOKIES_EXPIRE_TIME': cls.SESSION_COOKIES_EXPIRE_TIME,
                  'CACHE_HOST': cls.CACHE_HOST,
                  'CACHE_PORT': cls.CACHE_PORT,
                  'CACHE_EXPIRE_TIME': cls.CACHE_EXPIRE_TIME,
                  'ZIPS_PATH': cls.ZIPS_PATH
                  }
        return config

    @classmethod
    def reconfigure_values_for_tests(cls):
        cls.STORAGE_PATH = getenv('TEST_STORAGE_PATH')
        cls.DATABASE_URL = getenv('TEST_DATABASE_URL')
        cls.CACHE_PORT = getenv('TEST_CACHE_PORT')
        cls.ZIPS_PATH = getenv('TEST_ZIPS_PATH')
        cls.assert_not_none()

    @classmethod
    def assert_not_none(cls):
        assert cls.STORAGE_PATH is not None
        assert cls.STORAGE_ID_LEN is not None
        assert cls.DATABASE_URL is not None
        assert cls.SESSION_EXPIRE_TIME is not None
        assert cls.SESSION_COOKIES_EXPIRE_TIME is not None
        assert cls.CACHE_PORT is not None
        assert cls.CACHE_HOST is not None
        assert cls.CACHE_EXPIRE_TIME is not None
        assert cls.ZIPS_PATH is not None

Config.assert_not_none()