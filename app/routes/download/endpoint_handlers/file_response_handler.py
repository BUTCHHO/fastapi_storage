from fastapi.responses import FileResponse

from interfaces import IStorageReader, IArchivator, ILogger
from exceptions import APIEntityDoesNotExists, APIUnsupportedEntityType
from utils import get_encoded_string


class FileResponseHandler:
    def __init__(self, archivator, storage_reader, path_validator, path_joiner):
        self.archivator: IArchivator = archivator
        self.storage_reader: IStorageReader = storage_reader
        self.path_joiner = path_joiner
        self.ensurer = path_validator
        self.encode_string = get_encoded_string

    def _make_response(self, path_to_entity):
        str_path_to_entity = path_to_entity.__str__()
        entity_name = self.storage_reader.get_name(str_path_to_entity)
        encoded_entity_name = self.encode_string(entity_name)
        return FileResponse(path_to_entity,
                            filename=f'{entity_name}',
                            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_entity_name}"},
    )


    def get_zip_file_response(self, path_in_storage_with_id):
        absolute_path_dir = self.storage_reader.join_with_root_path(path_in_storage_with_id)
        zip_path = self.archivator.create_large_zip(absolute_path_dir)
        return self._make_response(zip_path)


    def get_file_response(self, path_in_storage_with_id):
        absolute_path_file = self.storage_reader.join_with_root_path(path_in_storage_with_id)
        return self._make_response(absolute_path_file)


    def get_response(self, storage_id, entity_path_in_storage):
        entity_path_in_storage = self.path_joiner.join_paths(storage_id, entity_path_in_storage)
        self.ensurer.ensure_path_safety(storage_id, entity_path_in_storage)
        if not self.ensurer.is_exists(entity_path_in_storage):
            raise APIEntityDoesNotExists(entity_path_in_storage)
        if self.storage_reader.is_dir(entity_path_in_storage):
            return self.get_zip_file_response(entity_path_in_storage)
        elif self.storage_reader.is_file(entity_path_in_storage):
            return self.get_file_response(entity_path_in_storage)
        else:
            raise APIUnsupportedEntityType(entity_path_in_storage=entity_path_in_storage)

