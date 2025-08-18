class TooManyFiles(Exception):
    def __init__(self):
        msg = 'Too many files uploaded'
        super().__init__(msg)

class PathGoesBeyondLimits(Exception):
    def __init__(self, path):
        self.msg = f'path {path} goes beyond permitted limits'
        super().__init__(self.detail)

class EntityDoesNotExists(Exception):
    def __init__(self, entity_path):
        self.msg = f"File or directory does not exists at {entity_path}"
        super().__init__(self.msg)

class EntityIsNotADir(Exception):
    def __init__(self, entity_path):
        self.detail = f'Entity at {entity_path} is not a directory'
        super().__init__(self.detail)


class UserStorageAlreadyExists(Exception):
    def __init__(self):
        self.detail = 'Storage for this user already exists. Failed to create new storage'
        super().__init__(self.detail)

class DirectoryAlreadyExists(Exception):
    def __init__(self):
        self.detail = f'Directory already exists'
        super().__init__(self.detail)

class UnsupportedEntityType(Exception):
    def __init__(self, path=None):
        self.detail = f'Entity type is not supported {path}'
        super().__init__(self.detail)