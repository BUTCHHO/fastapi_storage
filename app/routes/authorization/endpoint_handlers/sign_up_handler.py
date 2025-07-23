from exceptions import APIUserAlreadyExists, APIUserStorageAlreadyExists
from auth.exceptions import UserAlreadyExists
from interfaces import IStorageWriter

class SignUpHandler:
    def __init__(self, user_registrator, storage_writer, user_reader):
        self.user_registrator = user_registrator
        self.storage_writer: IStorageWriter = storage_writer
        self.user_reader = user_reader


    async def sign_up(self, params):
        try:
            await self.user_registrator.create_user(params.name, params.password)
            user = await self.user_reader.get_by_kwargs(name = params.name)
            self.create_user_storage(user.storage_id)
        except UserAlreadyExists:
            raise APIUserAlreadyExists(params.name)

    def create_user_storage(self, storage_id):
        try:
            self.storage_writer.create_dir('', storage_id, exist_ok=False)
        except FileExistsError:
            raise APIUserStorageAlreadyExists