from pathlib import Path


class PathJoiner:
    def __init__(self, root_path):
        self.root_path = root_path


    @property
    def root(self):
        return self.root_path


    def join_paths(self, path1, path2):
        new_path = Path(path1, path2)
        return new_path.__str__()

    def join_with_root_path(self, path:str):
        return self.join_paths(self.root_path, path)

    def create_absolute_entity_path(self, storage_id, entity_path_in_storage):
        if entity_path_in_storage is None:
            entity_path_in_storage = ''
        abs_user_dir_path = self.create_absolute_user_dir_path(storage_id)
        abs_path = self.join_paths(abs_user_dir_path, entity_path_in_storage)
        return abs_path

    def create_absolute_user_dir_path(self, user_id):
        user_id = str(user_id)
        return self.join_with_root_path(user_id)