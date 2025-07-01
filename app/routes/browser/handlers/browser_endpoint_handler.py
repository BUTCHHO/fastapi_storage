from fastapi import HTTPException
from markdown_it.common.entities import entities

from exceptions import APIEntityDoesNotExists, EntityDoesNotExists
from interfaces import ILogger, IStorageReader, IPathCutter


class BrowserEndpointHandler:
    def __init__(self, storage_reader, logger, path_joiner, path_cutter, path_ensurer):
        self.storage_reader: IStorageReader = storage_reader
        self.path_ensurer = path_ensurer
        self.logger: ILogger = logger
        self.path_joiner = path_joiner
        self.path_cutter: IPathCutter = path_cutter

    def _get_abs_path(self, user_id, path_to_dir):
        path_with_user_id = self.path_joiner.join_paths(user_id, path_to_dir)
        return self.storage_reader.join_with_root_path(path_with_user_id)

    def _cut_user_id_from_entitynames(self, entities: list[str]):
        cut_entities = [self.path_cutter.remove_id_from_rel_path(entity) for entity in entities]
        return cut_entities

    def _get_all_entitynames_in_dir(self, rel_dir_path):
        entitynames = self.storage_reader.get_all_entitynames_in_dir(rel_dir_path)
        return self._cut_user_id_from_entitynames(entitynames)

    def get_list_of_entities(self, user_id, path_in_storage: str | None):
        try:
            if path_in_storage is None:
                path_in_storage = ''
            self.path_ensurer.ensure_path_safety(user_id, path_in_storage)
            path_in_storage_with_id = self.path_joiner.join_paths(str(user_id), path_in_storage)
            entitynames = self._get_all_entitynames_in_dir(path_in_storage_with_id)
            return entitynames
        except EntityDoesNotExists:
            raise APIEntityDoesNotExists(path_in_storage)
        except Exception as e:
            self.logger.log(e)

    def _recursively_get_entities_by_pattern(self, pattern:str, searching_in):
        entities = self.storage_reader.find_entities_path(searching_in, pattern)
        return entities

    def search_entities_by_pattern(self, user_id: str, pattern: str, searching_in: str):
        try:
            pattern = f'{pattern}*'
            if searching_in is None:
                searching_in = ''
            self.path_ensurer.ensure_path_safety(user_id, searching_in)
            searching_in_path_with_id = self.path_joiner.join_paths(user_id, searching_in)
            entities = self._recursively_get_entities_by_pattern(pattern, searching_in_path_with_id)
            return self._cut_user_id_from_entitynames(entities)
        except Exception as e:
            self.logger.log(e)