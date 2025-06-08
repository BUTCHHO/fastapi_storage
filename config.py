from dotenv import load_dotenv
from os import getenv
from exceptions import StoragePathIsNone

load_dotenv('.env')

STORAGE_PATH = getenv('STORAGE_PATH')


if STORAGE_PATH is None:
    raise StoragePathIsNone

