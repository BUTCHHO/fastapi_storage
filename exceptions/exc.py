class StoragePathIsNone(Exception):
    def __init__(self):
        msg = 'STORAGE_PATH value from .env file is None. Must be filled'
        super().__init__(msg)

class NotAUserId(Exception):
    def __init__(self, path:str):
        msg = f'path {path} dont starts with user_id. Must look like \'1/folder/file.txt\''
        super().__init__(msg)