from os import getenv

from path_explorator import PathGoesBeyondLimits, EntityDoesNotExists
from path_explorator import PathValidator

STORAGE_PATH = getenv('STORAGE_PATH')

path_validator = PathValidator(STORAGE_PATH)

def raise_if_goes_beyond_limits(requesting_path: str):
    if path_validator.is_goes_beyond_limits(requesting_path):
        raise PathGoesBeyondLimits(requesting_path)

def raise_if_entity_dont_exists(path:str):
    if not path_validator.is_exists(path):
        raise EntityDoesNotExists(path)

def raise_if_path_invalid(path:str):
    raise_if_goes_beyond_limits(path)
    raise_if_entity_dont_exists(path)



