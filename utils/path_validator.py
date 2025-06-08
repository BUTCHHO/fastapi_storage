from exceptions import APIPathGoesBeyondLimits
from path_explorator import PathGoesBeyondLimits, EntityDoesNotExists, PathValidator


class PathValidEnsurer(PathValidator):
    def __init__(self, storage_path):
        super().__init__(storage_path)

    def raise_if_goes_beyond_limits(self, requesting_path: str):
        if self.is_goes_beyond_limits(requesting_path):
            raise PathGoesBeyondLimits(requesting_path)

    def raise_if_entity_dont_exists(self, path:str):
        if not self.is_exists(path):
            raise EntityDoesNotExists(path)

    def raise_if_path_invalid(self, path:str):
        self.raise_if_goes_beyond_limits(path)
        self.raise_if_entity_dont_exists(path)

    def ensure_path_safety_on_endpoint_level(self, abs_path, path_in_storage):
        try:
            self.raise_if_goes_beyond_limits(abs_path)
        except PathGoesBeyondLimits:
            raise APIPathGoesBeyondLimits(path_in_storage)


