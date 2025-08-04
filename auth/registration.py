from .pydantic_models import User
from .exceptions import UserAlreadyExists

class Registrator:
    def __init__(self, user_actor, user_reader, hash_maker):
        self.user_actor = user_actor
        self.user_reader = user_reader
        self.hash_maker = hash_maker

    async def registrate_user(self, user_model: User):
        if await self.user_reader.get_record_by(name=user_model.name):
            raise UserAlreadyExists
        hash_psw = self.hash_maker.make_hash(user_model.password)
        await self.user_actor.make_record_and_write(name=user_model.name, password=hash_psw)
        return True