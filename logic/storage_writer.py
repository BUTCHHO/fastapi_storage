from path_explorator import DirectoryActor


class StorageWriter(DirectoryActor):
    def __init__(self, root_dir):
        super().__init__(root_dir)