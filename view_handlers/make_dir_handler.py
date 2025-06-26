from interfaces import IStorageWriter
from exceptions import APIDirectoryAlreadyExists


class MakeDirHandler():
    def __init__(self, logger, storage_writer):
        self.logger = logger
        self.storage_writer: IStorageWriter = storage_writer

    def make_dir_in_storage(self, path, name):
        if path is None:
            path = ''
        try:
            self.storage_writer.create_dir(path, name)
        except FileExistsError:
            raise APIDirectoryAlreadyExists