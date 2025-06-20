from exceptions import SessionExpired, SessionDontExists

class UserGetter:
    def __init__(self, user_reader, session_reader, cacher, session_validator):
        self.session_reader = session_reader
        self.user_reader = user_reader
        self.cacher = cacher
        self.session_validator = session_validator


    def _get_user_from_db(self, user_id):
        return self.user_reader.get_by_kwargs(id=user_id)

    def _get_session_from_db(self, id):
        return self.session_reader.get_by_id(id)

    def _get_user_if_session_not_in_cache(self, session_id):
        session = self._get_session_from_db(session_id)
        if not session:
            raise SessionDontExists
        self.session_validator.validate_session_or_raise(session)
        return self._get_user_from_db(session.user_id)

    def get_user_by_session_id(self, session_id):
        user_id = (self.cacher.get_data(session_id))
        if not user_id:
            return self._get_user_if_session_not_in_cache(session_id)
        user_id = int(user_id)
        self.cacher.put_data(session_id, user_id)
        return self._get_user_from_db(user_id)

