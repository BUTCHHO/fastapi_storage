from exceptions import UserAlreadyExists
from psycopg2.errors import UniqueViolation

class UserRegistration:
    def __init__(self, db_reader, db_actor, hash_func, logger):
        self._reader = db_reader
        self._actor = db_actor
        self.hash_func = hash_func
        self.logger = logger

    def create_user(self, name, password):
        try:
            password = self.hash_func(password)
            self._actor.create_amd_write_record_to_db(name, password)
        except UniqueViolation:
            raise UserAlreadyExists(name)
        except Exception as e:
            self.logger.log(e)

