from interfaces import IPathValidator, ILogger, IStorageWriter

class UploadFileHandler:
    def __init__(self, storage_writer, validator, logger):
        self.storage_writer: IStorageWriter = storage_writer
        self.validator: IPathValidator = validator
        self.logger: ILogger = logger

    def join_abs_fpath_and_fname(self, abs_path, fname):
        return f'{abs_path}/{fname}'

    async def _iterate_and_save_files_to_storage(self, files: list, output_path):
        try:
            for file in files:
                abs_file_path_and_name = self.join_abs_fpath_and_fname(output_path, file.filename)
                await self.storage_writer.async_write_from_fastapi_uploadfile_to_file(file, abs_file_path_and_name)
        except Exception as e:
            self.logger.log(e)
            raise e

    async def save_files_to_storage(self, absolute_path, files: list):
        await self._iterate_and_save_files_to_storage(files, absolute_path)

