from .exceptions import UserAlreadyExists
from exceptions.database_repo import FieldUniqueViolation

class UserRegistration:
    def __init__(self,user_actor, hasher, logger):
        self._user_actor = user_actor
        self.hasher = hasher
        self.logger = logger

    async def create_user(self, name, password):
        try:
            password = self.hasher.generate_psw_hash(password)
            storage_id = self.hasher.generate_hash(16)
            await self._user_actor.create_and_write_record_to_db(name=name, password=password, storage_id=storage_id)
        except FieldUniqueViolation:
                raise UserAlreadyExists(name)
        except Exception as e:
            self.logger.log(e)


