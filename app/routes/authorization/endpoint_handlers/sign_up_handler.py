from exceptions import APIUserAlreadyExists, APIUserStorageAlreadyExists
from auth.exceptions import UserAlreadyExists
from interfaces import IStorageWriter
from auth.registration import Registrator

class SignUpHandler:
    def __init__(self, user_registrator, storage_writer, user_reader, user_actor, hasher, storage_id_len):
        self.user_registrator: Registrator = user_registrator
        self.storage_writer: IStorageWriter = storage_writer
        self.user_reader = user_reader
        self.user_actor = user_actor
        self.hasher = hasher
        self.STORAGE_ID_LEN = storage_id_len


    async def sign_up(self, params):
        try:
            await self.user_registrator.registrate_user(params.name, params.password)
            user = await self.user_reader.get_by_kwargs(name = params.name)
            await self.create_user_storage(user)
        except UserAlreadyExists:
            raise APIUserAlreadyExists(params.name)

    async def create_user_storage(self, user):
        try:
            storage_id = self.hasher.generate_hash(self.STORAGE_ID_LEN)
            self.storage_writer.create_dir('', storage_id, exist_ok=False)
            await self.user_actor.change_values_by_kwargs(new_values={'storage_id':storage_id}, name=user.name)
        except FileExistsError:
            raise APIUserStorageAlreadyExists
