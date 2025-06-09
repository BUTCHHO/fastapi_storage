from exceptions import NotAUserId

class PathCutter:

    def _get_id_part(self, path:str) -> str:
        max_split = 1
        return path.split('/', max_split)[0]

    def cut_user_id_from_storage_path(self, path: str):
        path = path.lstrip('/') # input path looks like /{id}/folder/file.txt. removing first slash
        id_part = self._get_id_part(path)
        if not id_part.isdigit():
            raise NotAUserId(path)
        return path.removeprefix(id_part)