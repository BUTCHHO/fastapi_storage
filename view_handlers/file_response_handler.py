from fastapi.responses import FileResponse
from fastapi import HTTPException
from interfaces import IStorageReader, IArchivator, ILogger, IPathValidator
from exceptions import APIPathGoesBeyondLimits, APIEntityDoesNotExists, APIUnsupportedEntityType
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
            raise e

    def get_zip_file_response(self, absolute_path_dir):
        try:
            zip_path = self.archivator.create_large_zip(absolute_path_dir)
            return self._make_response(zip_path)
        except Exception as e:
            self.logger.log(e)

    def get_file_response(self, absolute_path_file):
        return self._make_response(absolute_path_file)


    def get_response(self, absolute_entity_path, entity_path_in_storage):
        if not self.validator.is_exists(absolute_entity_path):
            raise EntityDoesNotExists
        if self.storage_reader.is_dir(absolute_entity_path):
            return self.get_zip_file_response(absolute_entity_path)
        if self.storage_reader.is_file(absolute_entity_path):
            return self.get_file_response(absolute_entity_path)
        else:
            raise APIUnsupportedEntityType(entity_path_in_storage=entity_path_in_storage)

