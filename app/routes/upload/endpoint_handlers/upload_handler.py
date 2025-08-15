from exceptions.path_exc import TooManyFiles, EntityDoesNotExists
from interfaces import ILogger, IStorageWriter

class UploadFileHandler:
    def __init__(self, storage_writer, path_ensurer, logger, path_joiner):
        self.storage_writer: IStorageWriter = storage_writer
        self.path_ensurer = path_ensurer
        self.path_joiner = path_joiner
        self.logger: ILogger = logger
        self.max_upload_files = 20

    def create_rel_fpath_with_id(self, user_id, rel_path, fname:str):
        fname = fname.lstrip('/') #I DONT KNOW WHY BUT PATHLIB REFUSES TO JOIN PATHS/ IT JUST RETURNS FNAME AS IT WAS IF WE DONT REMOVE THIS SLASH
        fpath_and_name = self.join_fpath_and_fname(rel_path, fname)
        fpath_and_name = fpath_and_name.lstrip('/') # THE SAME PROBLEM
        return self.path_joiner.join_paths(user_id, fpath_and_name)

    def join_fpath_and_fname(self, fpath, fname):
        return f'{fpath}/{fname}'

    async def _iterate_and_save_files_to_storage(self, files: list, output_path, user_id):
        try:
            for file in files:
                rel_fpath_with_id = self.create_rel_fpath_with_id(user_id, output_path, file.filename)
                await self.storage_writer.async_write_from_fastapi_uploadfile_to_file(file, rel_fpath_with_id)
        except FileNotFoundError:
            raise EntityDoesNotExists(output_path)
        except Exception as e:
            self.logger.log(e)
            raise e

    async def save_files_to_storage(self, storage_id, path_in_storage, files: list):
        if len(files) > self.max_upload_files:
            raise TooManyFiles
        if path_in_storage is None:
            path_in_storage = ''
        self.path_ensurer.ensure_path_safety(storage_id, path_in_storage)
        await self._iterate_and_save_files_to_storage(files, path_in_storage, storage_id)

