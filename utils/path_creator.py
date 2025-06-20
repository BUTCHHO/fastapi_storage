from path_explorator import PathCreator


class PathJoiner(PathCreator):
    def __init__(self, root_path):
        self.root_path = root_path
        super().__init__()

    @property
    def root(self):
        return self.root_path

    def join_with_root_path(self, path:str | int):
        if isinstance(path, int):
            path = str(path)
        return self.join_paths(self.root_path, path)

    def create_absolute_path(self, user_id, entity_path_in_storage):
        if entity_path_in_storage == None:
            entity_path_in_storage = ''
        user_id = str(user_id)
        path_in_storage_with_id = self.join_paths(user_id, entity_path_in_storage)
        return self.join_with_root_path(path_in_storage_with_id)