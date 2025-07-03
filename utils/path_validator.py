from exceptions import APIPathGoesBeyondLimits
from path_explorator import PathGoesBeyondLimits, EntityDoesNotExists
from interfaces import IPathCutter
from pathlib import Path


class PathValidEnsurer:

    def __init__(self, root_dir, path_cutter, path_creator):
        self.path_cutter: IPathCutter = path_cutter
        self.path_creator = path_creator
        self.root_dir = root_dir

    def does_contain_uplinks(self, path:str | Path):
        path = Path(self.root_dir, path)
        if ('..', '.', './') in path.parts:
            return True
        return False

    def does_contain_symlinks_and_uplinks(self, path:str):
        path = Path(self.root_dir, path)
        if path.is_symlink() and self.does_contain_uplinks(path):
            return True
        return False


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


    def raise_if_goes_beyond_limits(self, abs_path: str, storage_id, requesting_path:str):
        user_directory = self.path_creator.create_absolute_user_dir_path(storage_id)
        if self.is_goes_beyond_limits(abs_path):
            raise PathGoesBeyondLimits(requesting_path)
        if not self.is_path_rel_to_another_path(abs_path, user_directory):
            raise PathGoesBeyondLimits(requesting_path)

    def raise_if_entity_dont_exists(self, path:str):
        if not self.is_exists(path):
            raise EntityDoesNotExists(path)

    def ensure_path_safety(self, storage_id: int, path_in_storage: str):
        try:
            abs_path = self.path_creator.create_absolute_path(storage_id, path_in_storage)
            self.raise_if_goes_beyond_limits(abs_path, storage_id, path_in_storage)
        except PathGoesBeyondLimits:
            raise APIPathGoesBeyondLimits(path_in_storage)


