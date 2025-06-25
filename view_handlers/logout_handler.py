from fastapi import Request, Response


class LogOutHandler:
    def __init__(self, session_deleter, logger):
        self.session_deleter = session_deleter
        self.logger = logger

    def logout_user(self, request: Request, response: Response):
        try:
            session_id = request.cookies.get('session_id')
            if session_id is None:
                return
            response.delete_cookie('session_id')
            self.session_deleter.delete_session(session_id)
        except Exception as e:
            self.logger.log(e)
            raise e
