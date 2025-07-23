from exceptions import APIPathGoesBeyondLimits
from exceptions import EntityDoesNotExists, PathGoesBeyondLimits
from interfaces import IPathCutter
from pathlib import Path


class PathValidEnsurer:

    def __init__(self, root_dir, path_cutter, path_creator):
        self.path_cutter: IPathCutter = path_cutter
        self.path_joiner = path_creator
        self.root_dir = root_dir

    def is_goes_beyond_limits(self, requesting_path: str | None):
        return not self.is_path_rel_to_another_path(requesting_path, self.root_dir.__str__())


    def is_path_rel_to_another_path(self, path: str | None, relative_to_path: str | None):
        if path is None:
            path = ''
        if relative_to_path is None:
            relative_to_path = ''
        path = Path(path).resolve()
        relative_to_path = Path(relative_to_path)
        if path.is_relative_to(relative_to_path):
           return True
        return False

    @property
    def root(self):
        return self.root_dir.__str__()

    def is_exists(self, path: str) -> bool:
        """
        Checks if specified path exists
        :param path: path to the entity checking
        :return: exists or not True or False
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.exists()


    def is_file(self, path: str) -> bool:
        """
        Checks if specified entity is FILE
        :param path: path to entity
        :return: file or not
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.is_file()


    def is_dir(self, path: str) -> bool:
        """
        Checks if specified entity is DIRECTORY/FOLDER
        :param path: path to entity
        :return: dir or not
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.is_dir()



    def raise_if_goes_beyond_limits(self, limiting_path: str, requesting_path:str):
        """

        :param limiting_path:
        :param requesting_path:
        :return:
        """
        if self.is_goes_beyond_limits(limiting_path):
            raise PathGoesBeyondLimits(requesting_path)
        if not self.is_path_rel_to_another_path(requesting_path, limiting_path):
            raise PathGoesBeyondLimits(requesting_path)

    def raise_if_entity_dont_exists(self, path:str):
        if not self.is_exists(path):
            raise EntityDoesNotExists(path)

    def ensure_path_safety(self, storage_id: int, path_in_storage: str):
        """
        :raises: PathGoesBeyondLimits
        """
        abs_requesting_path = self.path_joiner.create_absolute_entity_path(storage_id, path_in_storage)
        abs_limiting_path = self.path_joiner.create_absolute_user_dir_path(storage_id)
        self.raise_if_goes_beyond_limits(abs_limiting_path, abs_requesting_path)



