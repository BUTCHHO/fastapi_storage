class RepositoryFilesCountError(Exception):
    def __init__(self, msg='repository files count error!'):
        super().__init__(msg)

class RepositoryDirsCountError(Exception):
    def __init__(self, msg='repository dirs count error!'):
        super().__init__(msg)