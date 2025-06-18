from interfaces import IModelActor

class SessionMaker:
    def __init__(self, session_expire_time, session_access, time_handler, hasher, cacher):
        self.expire_time = session_expire_time
        self._access: IModelActor = session_access
        self.time_handler = time_handler
        self.hasher = hasher
        self.cacher = cacher

    def _get_expire_date(self):
        return self.time_handler.add_days_to_current_date(self.expire_time)

    def _create_session_obj(self, user_id, username):
        session_id = self._create_session_id(username)
        expire_date = self._get_expire_date()
        session_record = self._access.create_record(id=session_id, expire_date=expire_date, user_id=user_id)
        return session_record

    def _create_session_id(self):
        hashed_id = self.hasher.create_session_id_hash()
        return hashed_id

    def create_session(self, user_id, username):
        session = self._create_session_obj(user_id, username)
        self._access.write_record_to_db(session)
        self.cacher.put_data(session.id, user_id)
        return session