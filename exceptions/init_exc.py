class StoragePathIsNone(Exception):
    def __init__(self):
        msg = 'STORAGE_PATH value from .env file is None. Must be filled'
        super().__init__(msg)