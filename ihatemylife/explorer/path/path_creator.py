from pathlib import Path



class PathCreator:
    def __init__(self):
        pass
    
    def smart_path(self, path1, path2):
        if isinstance(path1, str) and isinstance(path2, str):
            return Path(f"{path1}/{path2}")
        return Path(path1 / path2)
            

    def join_strlike_path(self, path1, path2):
        new_path = path1 / path2
        return new_path

    def join_strlike_path_to_pathliblike(self, path1, path2):
        new_path = Path(path1 / path2)
        return new_path

    def join_path(self, path1, path2):
        new_path = Path(path1 / path2)
        return new_path

