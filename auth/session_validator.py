from interfaces import ITimeHandler
from .exceptions import SessionExpired

class SessionValidator:
    def __init__(self, time_handler, session_deleter):
        self.time_handler: ITimeHandler = time_handler
        self.session_deleter = session_deleter

    def is_session_expired(self, session_expire_date):
        if self.time_handler.is_date_future(session_expire_date):
            return False
        return True

    async def validate_session_or_raise(self, session):
        if self.is_session_expired(session.expire_date):
            await self.session_deleter.delete_session(session)
            raise SessionExpired
        return True
