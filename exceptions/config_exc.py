class StoragePathIsNone(Exception):
    def __init__(self):
        msg = 'STORAGE_PATH value from .env file is None. Must be filled'
        super().__init__(msg)

class DatabaseUrlIsNone(Exception):
    def __init__(self):
        msg = 'DATABASE_URL value from .env file is None. Must be filled'
        super().__init__(msg)

class CachePortIsNone(Exception):
    def __init__(self):
        msg = 'CACHE_PORT value from .env file is None. Must be filled'
        super().__init__(msg)

class CacheHostIsNone(Exception):
    def __init__(self):
        msg = 'CACHE_HOST value from .env file is None. Must be filled'
        super().__init__(msg)

class CacheExpireTimeIsNone(Exception):
    def __init__(self):
        msg = 'CACHE_EXPIRE_TIME value from .env file is None. Must be filled'
        super().__init__(msg)

class SessionMakerKeyIsNone(Exception):
    def __init__(self):
        msg = 'SESSION_MAKER_KEY value from .env file is None. Must be filled'
        super().__init__(msg)