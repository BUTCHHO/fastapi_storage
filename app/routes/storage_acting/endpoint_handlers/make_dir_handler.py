from path_explorator import EntityDoesNotExists, EntityIsNotADir

from interfaces import IStorageWriter
from exceptions import APIEntityIsNotADir, APIEntityDoesNotExists



class MakeDirHandler:
    def __init__(self, storage_writer, path_joiner, path_ensurer):
        self.storage_writer: IStorageWriter = storage_writer
        self.path_joiner = path_joiner
        self.path_ensurer = path_ensurer

    def make_dir_in_storage(self,storage_id, path, name):
        if path is None:
            path = ''
        try:
            self.path_ensurer.ensure_path_safety(storage_id, path)
            path_with_storage_id = self.path_joiner.join_paths(storage_id, path)
            self.storage_writer.create_dir(path_with_storage_id, name)
        except EntityDoesNotExists:
            raise APIEntityDoesNotExists(path)
        except EntityIsNotADir:
            raise APIEntityIsNotADir(path)