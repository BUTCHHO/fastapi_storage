from exceptions import NotAUserId

class PathCutter:
    def __init__(self, root_path):
        self.root_path = root_path

    def get_user_id_from_abs_path(self, abs_path: str):
        path = abs_path.removeprefix(self.root_path)
        id = self.get_user_id_part_from_rel_path(path)
        if not id.isdigit():
            raise NotAUserId(abs_path)
        return id

    def get_user_id_part_from_rel_path(self, path:str) -> str:
        #path must look like '/<id>/some/path or '<id>/some/path
        if path[0] == '/':
            return path.split('/')[1]
        return path.split('/')[0]

    def remove_id_from_rel_path(self, rel_path):
        if rel_path[0] == '/':
            return rel_path[2:]
        return rel_path[1:]

