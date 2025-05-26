from os import getenv
from path_explorator.utils import raise_if_path_goes_beyond_limits
STORAGE_PATH = getenv('STORAGE_PATH')

def validate_path(path: str):
    if not raise_if_path_goes_beyond_limits(STORAGE_PATH, path):
        return True
