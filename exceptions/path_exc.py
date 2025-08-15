from path_explorator.exceptions import EntityDoesNotExists, EntityIsNotADir, PathGoesBeyondLimits

class TooManyFiles(Exception):
    def __init__(self):
        msg = 'Too many files uploaded'
        super().__init__(msg)

class UserStorageAlreadyExists():
    def __init__(self):
        detail = 'Storage for this user already exists. Failed to create new storage'
        super().__init__( detail)

class DirectoryAlreadyExists():
    def __init__(self, path):
        detail = f'Directory at {path} already exists'
        super().__init__(detail)