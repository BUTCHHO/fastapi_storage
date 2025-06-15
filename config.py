from dotenv import load_dotenv
from os import getenv
from exceptions import StoragePathIsNone, DatabaseUrlIsNone

load_dotenv('.env')

STORAGE_PATH = getenv('STORAGE_PATH')
DATABASE_URL = getenv('DATABASE_URL')

if STORAGE_PATH is None:
    raise StoragePathIsNone
if DATABASE_URL is None:
    raise DatabaseUrlIsNone
