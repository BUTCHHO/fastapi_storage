from dotenv import load_dotenv
from os import getenv
from exceptions import StoragePathIsNone, DatabaseUrlIsNone

load_dotenv('.env')

STORAGE_PATH = getenv('STORAGE_PATH')
DATABASE_URL = getenv('DATABASE_URL')
SESSION_MAKER_KEY = getenv('SESSION_MAKER_KEY')

if STORAGE_PATH is None:
    raise StoragePathIsNone
if DATABASE_URL is None:
    raise DatabaseUrlIsNone
if SESSION_MAKER_KEY is None:
    print('WARNING session_maker_key is None WARNING')

