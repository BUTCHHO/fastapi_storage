from interfaces import IStorageWriter
from exceptions import APIDirectoryAlreadyExists


class MakeDirHandler():
    def __init__(self, logger, storage_writer, path_joiner, path_ensurer):
        self.logger = logger
        self.storage_writer: IStorageWriter = storage_writer
        self.path_joiner = path_joiner
        self.path_ensurer = path_ensurer

    def make_dir_in_storage(self,user_id, path, name):
        if path is None:
            path = ''
        try:
            self.path_ensurer.ensure_path_safety(user_id, path)
            path_with_user_id = self.path_joiner.join_paths(str(user_id), path)
            self.storage_writer.create_dir(path_with_user_id, name)
        except FileExistsError:
            raise APIDirectoryAlreadyExists