class NotAUserId(Exception):
    def __init__(self, path:str):
        msg = f'path {path} dont starts with user_id. Must look like \'1/folder/file.txt\''
        super().__init__(msg)