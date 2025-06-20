from interfaces import ITimeHandler
from exceptions import SessionExpired

class SessionValidator:
    def __init__(self, time_handler):
        self.time_handler: ITimeHandler = time_handler

    def is_session_expired(self, session_expire_date):
        if self.time_handler.is_date_future(session_expire_date):
            return False
        return True

    def validate_session_or_raise(self, session):
        if self.is_session_expired(session.expire_date):
            raise SessionExpired()
        return True
