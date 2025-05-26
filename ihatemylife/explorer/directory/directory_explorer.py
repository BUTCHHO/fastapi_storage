from pathlib import Path
from ...exceptions import EntityDoesNotExists, NotADir
from ..path import PathCreator

path_creator = PathCreator()
smart_path = path_creator.smart_path

class DirectoryExplorer:
    def __init__(self, root_dir = ''):
        self.root_dir = root_dir

    def get_all_filenames_in_dir(self, dirpath: str):
        path = smart_path(self.root_dir, dirpath)
        if not path.exists():
            raise EntityDoesNotExists(dirpath)
        if not path.is_dir():
            raise NotADir(dirpath)

        filenames = [fname for fname in path.iterdir() if fname.is_file()]
        return filenames

    def get_all_entitynames_in_dir(self, dirpath:str):
        path = smart_path(self.root_dir, dirpath)
        if not path.exists():
            raise EntityDoesNotExists(dirpath)
        if not path.is_dir():
            raise NotADir(dirpath)


        entities_names = list(path.iterdir())
        return entities_names

    def is_exists(self, path:str):
        entity = Path(path)
        return entity.exists()

    def find_file_path(self, searching_in, fname):
        searchable_dir  = smart_path(self.root_dir, searching_in)
        for entity in searchable_dir.rglob(fname):
            print(f"entity {entity}")

