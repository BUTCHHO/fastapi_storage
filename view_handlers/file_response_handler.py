from fastapi.responses import FileResponse
from fastapi import HTTPException
from logic import StorageReader
from path_explorator import EntityDoesNotExists, PathGoesBeyondLimits
from utils import get_encoded_string, raise_if_path_invalid


class FileResposeHandler:
    def __init__(self, archivator, storage_reader):
        self.archivator = archivator
        self.storage_reader: StorageReader = storage_reader
        self.raise_if_invalid = raise_if_path_invalid
        self.encode_string = get_encoded_string

    def _make_response(self, path_to_entity):
        str_path_to_entity = path_to_entity.__str__()
        entity_name = self.storage_reader.get_name(str_path_to_entity)
        encoded_entity_name = self.encode_string(entity_name)
        return FileResponse(path_to_entity,
                            filename=f'{entity_name}',
                            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_entity_name}"},
)

    def get_zip_file_response(self, absolute_path_dir):
        zip_path = self.archivator.create_large_zip(absolute_path_dir)
        return self._make_response(zip_path)

    def get_file_response(self, absolute_path_file):
        return self._make_response(absolute_path_file)

    def validate_path(self, absolute_path, entity_path_in_storage):
        try:
            self.raise_if_invalid(absolute_path)
        except PathGoesBeyondLimits:
            raise HTTPException(status_code=403,
                                detail={"message": f'path {entity_path_in_storage} goes beyond permitted limits', "code":"path_goes_beyond_limits"})
        except EntityDoesNotExists:
            raise HTTPException(status_code=404,
                                detail={"message": f'entity at {entity_path_in_storage} does not exists', "code":'entity_does_not_exists'})

    def get_response(self, entity_path_in_storage):
        absolute_path = self.storage_reader.join_with_root_path(entity_path_in_storage)
        self.validate_path(absolute_path, entity_path_in_storage)
        if self.storage_reader.is_dir(entity_path_in_storage):
            return self.get_zip_file_response(absolute_path)
        if self.storage_reader.is_file(entity_path_in_storage):
            return self.get_file_response(absolute_path)
        else:
            raise HTTPException(status_code=400, detail={"message":f'unsupported entity type {entity_path_in_storage}', "code":'unsupported_entity_type'})