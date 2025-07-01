from .exceptions import UserAlreadyExists
from exceptions.database_repo import FieldUniqueViolation

class UserRegistration:
    def __init__(self,user_actor, hasher, logger):
        self._user_actor = user_actor
        self.hasher = hasher
        self.logger = logger

    def create_user(self, name, password):
        try:
            password = self.hasher.generate_psw_hash(password)
            self._user_actor.create_and_write_record_to_db(name=name, password=password)
        except FieldUniqueViolation:
                raise UserAlreadyExists(name)
        except Exception as e:
            self.logger.log(e)


