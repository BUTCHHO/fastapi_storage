from interfaces import ITimeHandler


class SessionValidator:
    def __init__(self, time_handler):
        self.time_handler: ITimeHandler = time_handler

    def check_if_session_expired(self, session_expire_date):
        if self.time_handler.is_date_future(session_expire_date):
            return False
        return True

