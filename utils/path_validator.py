from os import getenv

from path_explorator import PathGoesBeyondLimits, EntityDoesNotExists
from path_explorator import PathValidator

class PathValidEnsurer(PathValidator):
    def __init__(self, STORAGE_PATH):
        super().__init__(STORAGE_PATH)

    def raise_if_goes_beyond_limits(self, requesting_path: str):
        if self.is_goes_beyond_limits(requesting_path):
            raise PathGoesBeyondLimits(requesting_path)

    def raise_if_entity_dont_exists(self, path:str):
        if not self.is_exists(path):
            raise EntityDoesNotExists(path)

    def raise_if_path_invalid(self, path:str):
        self.raise_if_goes_beyond_limits(path)
        self.raise_if_entity_dont_exists(path)


