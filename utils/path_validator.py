from exceptions import APIPathGoesBeyondLimits
from path_explorator import PathGoesBeyondLimits, EntityDoesNotExists, PathValidator
from interfaces import IPathCutter


class PathValidEnsurer(PathValidator):

    def __init__(self, storage_path, path_cutter, path_creator):
        self.path_cutter: IPathCutter = path_cutter
        self.path_creator = path_creator
        super().__init__(storage_path)

    def raise_if_goes_beyond_limits(self, abs_path: str, user_id, requesting_path:str):
        user_directory = self.path_creator.create_absolute_user_dir_path(user_id)
        if self.is_goes_beyond_limits(abs_path):
            raise PathGoesBeyondLimits(requesting_path)
        if not self.is_path_rel_to_another_path(abs_path, user_directory):
            raise PathGoesBeyondLimits(requesting_path)

    def raise_if_entity_dont_exists(self, path:str):
        if not self.is_exists(path):
            raise EntityDoesNotExists(path)

    def ensure_path_safety_on_endpoint_level(self, abs_path: str, user_id: int, path_in_storage: str):
        try:
            self.raise_if_goes_beyond_limits(abs_path, user_id, path_in_storage)
        except PathGoesBeyondLimits:
            raise APIPathGoesBeyondLimits(path_in_storage)


