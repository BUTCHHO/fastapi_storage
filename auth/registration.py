from .pydantic_models import User
from .exceptions import UserAlreadyExists

class Registrator:
    def __init__(self, user_actor, user_reader, hash_maker):
        self.user_actor = user_actor
        self.user_reader = user_reader
        self.hash_maker = hash_maker

    async def registrate_user(self, name, password):
        if await self.user_reader.get_by_kwargs(name=name):
            raise UserAlreadyExists
        hash_psw = self.hash_maker.generate_psw_hash(password)
        await self.user_actor.create_and_write_record_to_db(name=name, password=hash_psw)
        return True