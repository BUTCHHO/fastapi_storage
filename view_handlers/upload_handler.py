from fastapi import HTTPException
from path_explorator import PathGoesBeyondLimits
from interfaces import IPathValidator, ILogger, IStorageReader, IStorageWriter

class UploadFileHandler:
    def __init__(self, storage_reader, storage_writer, validator, logger):
        self.storage_reader: IStorageReader = storage_reader
        self.storage_writer: IStorageWriter = storage_writer
        self.validator: IPathValidator = validator
        self.logger: ILogger = logger

    def ensure_path_valid_or_httpexception(self, abs_path, relative_path=None):
        try:
            self.validator.raise_if_goes_beyond_limits(abs_path)
        except PathGoesBeyondLimits:
            raise HTTPException(status_code=403, detail={"message": f'path {relative_path} goes beyond limits', "code": 'path_goes_beyond_limits'})

    async def _iterate_and_save_files_to_storage(self, files: list, output_path):
        try:
            for file in files:
                abs_file_path_and_name = f'{output_path}/{file.filename}'
                await self.storage_writer.async_write_from_fastapi_uploadfile_to_file(file, abs_file_path_and_name)
        except Exception as e:
            self.logger.log(e)

    async def save_files_to_storage(self, path, files: list):
        absolute_path = self.storage_reader.join_with_root_path(path)
        self.ensure_path_valid_or_httpexception(absolute_path, path)
        await self._iterate_and_save_files_to_storage(files, absolute_path)

