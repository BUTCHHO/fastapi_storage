from fastapi import HTTPException
from path_explorator import PathGoesBeyondLimits

from exceptions import APIEntityDoesNotExists, EntityDoesNotExists, APIPathGoesBeyondLimits
from interfaces import ILogger, IStorageReader, IPathCutter


class BrowserEndpointHandler:
    def __init__(self, storage_reader, path_joiner, path_cutter, path_ensurer):
        self.storage_reader: IStorageReader = storage_reader
        self.path_ensurer = path_ensurer
        self.path_joiner = path_joiner
        self.path_cutter: IPathCutter = path_cutter

    def _get_abs_path(self, storage_path, path_to_dir):
        path_with_storage_id = self.path_joiner.join_paths(storage_path, path_to_dir)
        return self.storage_reader.join_with_root_path(path_with_storage_id)

    def _get_all_entitynames_in_dir(self, rel_dir_path):
         return self.storage_reader.get_all_entitynames_in_dir(rel_dir_path)


    def get_list_of_entities(self, storage_id, path_in_storage: str | None):

        if path_in_storage is None:
            path_in_storage = ''
        self.path_ensurer.ensure_path_safety(storage_id, path_in_storage)
        path_in_storage_with_id = self.path_joiner.join_paths(storage_id, path_in_storage)
        entitynames = self._get_all_entitynames_in_dir(path_in_storage_with_id)
        return entitynames


    def _recursively_get_entities_by_pattern(self, pattern:str, searching_in):
        entities = self.storage_reader.find_entities_path(searching_in, pattern)
        return entities

    async def search_entities_by_pattern(self, storage_id: str, pattern: str, searching_in: str):
        pattern = f'{pattern}*'
        if searching_in is None:
            searching_in = ''
        self.path_ensurer.ensure_path_safety(storage_id, searching_in)
        searching_in_path_with_id = self.path_joiner.join_paths(storage_id, searching_in)
        entities = self._recursively_get_entities_by_pattern(pattern, searching_in_path_with_id)
        return entities
