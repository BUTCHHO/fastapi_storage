from interfaces import IModelActor
from werkzeug.security import generate_password_hash

class SessionMaker:
    def __init__(self, session_expire_time, db_access, time_handler):
        self.expire_time = session_expire_time
        self._access: IModelActor = db_access
        self.time_handler = time_handler

    def _get_expire_date(self):
        return self.time_handler.add_days_to_current_date(self.expire_time)

    def _create_session_obj(self, user_id, username):
        session_id = self._create_session_id(username)
        expire_date = self._get_expire_date()
        session_record = self._access.create_record(id=session_id, expire_date=expire_date, user_id=user_id)
        return session_record

    def _create_session_id(self, username):
        length = 10
        hash_start_id = 17 #до этих символов идёт одинаковый текст по типу encrypt:4231:8:1$ причем цифры одинаковые всегда
        hash_end_id = 67 #использовать лишь часть хэша вместо всего будет экономнее
        hashed_id = generate_password_hash(username, salt_length=length)
        return hashed_id[hash_start_id:hash_end_id] #итого длина хэша на выходе 50 символов

    def create_session(self, user_id, username):
        session = self._create_session_obj(user_id, username)
        self._access.write_record_to_db(session)
