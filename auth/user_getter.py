from exceptions import SessionExpired, SessionDontExists

class UserGetter:
    def __init__(self, user_reader, cacher, time_handler):
        self.reader = user_reader
        self.cacher = cacher
        self.time_handler = time_handler


    def _get_user_from_db(self, user_id):
        return self.reader.get_record_by(user_id=user_id)

    def _get_session_from_db(self, id):
        return self.reader.get_record_by_id(id)

    def _get_user_if_session_not_in_cache(self, session_id):
        session = self.get_user_by_session_id(session_id)
        if not session:
            raise SessionDontExists
        if not self.time_handler.is_date_future(session.expire_date):
            raise SessionExpired
        return self._get_user_from_db(session.user_id)

    def get_user_by_session_id(self, session_id):
        user_id = self.cacher.get_data(session_id)
        if not user_id:
            return self._get_user_if_session_not_in_cache(session_id)
        return self._get_user_from_db(user_id)

