from interfaces import ILogger, IStorageReader, IPathJoiner

class StorageViewHandler:
    def __init__(self, storage_reader, logger, path_joiner):
        self.storage_reader: IStorageReader = storage_reader
        self.logger: ILogger = logger
        self.path_joiner: IPathJoiner = path_joiner

    def _get_abs_path(self, user_id, path_to_dir):
        path_with_user_id = self.path_joiner.join_paths(user_id, path_to_dir)
        return self.storage_reader.join_with_root_path(path_with_user_id)

    def _get_all_entitynames_in_dir(self, abs_dir_path):
        return self.storage_reader.get_all_entitynames_in_dir(abs_dir_path)

    def get_list_of_entities(self, abs_path):
        try:
            entitynames = self._get_all_entitynames_in_dir(abs_path)
            return entitynames
        except Exception as e:
            self.logger.log(e)