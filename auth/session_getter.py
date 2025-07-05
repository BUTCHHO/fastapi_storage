from auth.exceptions import SessionDontExists, SessionExpired


class SessionGetter:
    def __init__(self, session_reader, cacher, session_validator, session_deleter):
        self.session_reader = session_reader
        self.cacher = cacher
        self.session_validator = session_validator
        self.session_deleter = session_deleter

    def get_session_from_db(self, user_id):
        return self.session_reader.get_by_kwargs(user_id=user_id)

    def get_session_id_by_user_id(self, user_id):
        session = self.get_session_from_db(user_id)
        if session is None:
            raise SessionDontExists
        try:
            self.session_validator.validate_session_or_raise(session)
        except SessionExpired:
            self.session_deleter.delete_session(session)
            raise
        return session
