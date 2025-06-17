from exceptions import UserAlreadyExists
from psycopg2.errors import UniqueViolation

class UserRegistration:
    def __init__(self, db_reader, db_actor, hasher, logger):
        self._reader = db_reader
        self._actor = db_actor
        self.hasher = hasher
        self.logger = logger

    def create_user(self, name, password):
        try:
            password = self.hasher.generate_psw_hash(password)
            self._actor.create_and_write_record_to_db(name=name, password=password)
        except UniqueViolation:
            raise UserAlreadyExists(name)
        except Exception as e:
            self.logger.log(e)

