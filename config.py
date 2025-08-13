from dotenv import load_dotenv
from os import getenv
from pydantic_settings import BaseSettings

load_dotenv('.env')

class Config(BaseSettings):
    STORAGE_PATH: str
    STORAGE_ID_LEN: int
    DATABASE_URL: str
    SESSION_EXPIRE_TIME: str
    SESSION_COOKIES_EXPIRE_TIME: str
    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_EXPIRE_TIME: str
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

def reconfigure_values_for_tests():
    Config.STORAGE_PATH = getenv('TEST_STORAGE_PATH')
    Config.DATABASE_URL = getenv('TEST_DATABASE_URL')
    Config.CACHE_PORT = int(getenv('TEST_CACHE_PORT'))

