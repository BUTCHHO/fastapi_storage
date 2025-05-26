from os import getenv
from path_explorator import DirectoryActor

STORAGE_PATH = getenv('STORAGE_PATH')

class StorageWriter(DirectoryActor):
    def __init__(self):
        super().__init__(STORAGE_PATH)