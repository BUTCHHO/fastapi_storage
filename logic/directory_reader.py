from path_explorator import DirectoryExplorer
from os import getenv
from fastapi import UploadFile
from aiofiles import open as aio_open

STORAGE_PATH = getenv('STORAGE_PATH')
class StorageReader(DirectoryExplorer):
    def __init__(self, root_dir=STORAGE_PATH):
        super().__init__(root_dir)
