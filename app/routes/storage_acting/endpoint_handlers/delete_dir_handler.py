from interfaces import IStorageWriter
from exceptions import EntityDoesNotExists, PathGoesBeyondLimits, APIPathGoesBeyondLimits, APIEntityDoesNotExists


class DeleteEntityHandler:
    def __init__(self, path_ensurer, storage_writer, path_joiner, logger):
        self.path_ensurer = path_ensurer
        self.storage_writer: IStorageWriter = storage_writer
        self.path_joiner = path_joiner
        self.logger = logger

    def delete_entity(self, storage_id, path_in_storage):
        try:
            if path_in_storage is None:
                path_in_storage = ''
            path_with_user_id = self.path_joiner.join_paths(storage_id, path_in_storage)
            self.path_ensurer.ensure_path_safety(storage_id, path_in_storage)
            self.storage_writer.delete_entity(path_with_user_id)
        except PathGoesBeyondLimits:
            raise APIPathGoesBeyondLimits(path_in_storage)
        except EntityDoesNotExists:
            raise APIEntityDoesNotExists(path_in_storage)
        except Exception as e:
            self.logger.log(e)