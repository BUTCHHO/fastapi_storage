from exceptions import APIUserAlreadyExists, APIUserStorageAlreadyExists
from auth.exceptions import UserAlreadyExists
from interfaces import IStorageWriter

class SignUpHandler:
    def __init__(self, user_registrator, storage_writer, user_reader):
        self.user_registrator = user_registrator
        self.storage_writer: IStorageWriter = storage_writer
        self.user_reader = user_reader


    def sign_up(self, params):
        try:
            self.user_registrator.create_user(params.name, params.password)
            user = self.user_reader.get_by_kwargs(name = params.name)
            self.create_user_dir(user.id)
        except UserAlreadyExists:
            raise APIUserAlreadyExists(params.name)

    def create_user_dir(self, user_id):
        try:
            self.storage_writer.create_dir('', str(user_id), exist_ok=False)
        except FileExistsError:
            raise APIUserStorageAlreadyExists