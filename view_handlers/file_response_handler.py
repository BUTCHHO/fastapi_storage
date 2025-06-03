from fastapi.responses import FileResponse
from fastapi import HTTPException
from interfaces import IStorageReader, IArchivator, ILogger, IPathValidator
from path_explorator import EntityDoesNotExists, PathGoesBeyondLimits
from utils import get_encoded_string


class FileResponseHandler:
    def __init__(self, archivator, storage_reader, logger, path_validator):
        self.archivator: IArchivator = archivator
        self.storage_reader: IStorageReader = storage_reader
        self.logger: ILogger = logger
        self.validator: IPathValidator = path_validator
        self.encode_string = get_encoded_string

    def _make_response(self, path_to_entity):
        try:
            str_path_to_entity = path_to_entity.__str__()
            entity_name = self.storage_reader.get_name(str_path_to_entity)
            encoded_entity_name = self.encode_string(entity_name)
            return FileResponse(path_to_entity,
                                filename=f'{entity_name}',
                                headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_entity_name}"},
    )
        except Exception as e:
            self.logger.log(e)

    def get_zip_file_response(self, absolute_path_dir):
        try:
            zip_path = self.archivator.create_large_zip(absolute_path_dir)
            return self._make_response(zip_path)
        except Exception as e:
            self.logger.log(e)

    def get_file_response(self, absolute_path_file):
        return self._make_response(absolute_path_file)

    def ensure_path_valid_or_httpexception(self, absolute_path, entity_path_in_storage):
        try:
            self.validator.raise_if_path_invalid(absolute_path)
        except PathGoesBeyondLimits:
            raise HTTPException(status_code=403,
                                detail={"message": f'path {entity_path_in_storage} goes beyond permitted limits', "code":"path_goes_beyond_limits"})
        except EntityDoesNotExists:
            raise HTTPException(status_code=404,
                                detail={"message": f'entity at {entity_path_in_storage} does not exists', "code":'entity_does_not_exists'})

    def get_response(self, entity_path_in_storage):
        absolute_path = self.storage_reader.join_with_root_path(entity_path_in_storage)
        self.ensure_path_valid_or_httpexception(absolute_path, entity_path_in_storage)
        if self.storage_reader.is_dir(entity_path_in_storage):
            return self.get_zip_file_response(absolute_path)
        if self.storage_reader.is_file(entity_path_in_storage):
            return self.get_file_response(absolute_path)
        else:
            raise HTTPException(status_code=400, detail={"message":f'unsupported entity type {entity_path_in_storage}', "code":'unsupported_entity_type'})
