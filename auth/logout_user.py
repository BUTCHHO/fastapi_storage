class UserLogout:
    def __init__(self, session_deleter):
        self.session_deleter = session_deleter



    def logout_user(self, request, response):
        """
        :param response: something to get cookies from
        :param request: something to put/delete cookies from
        if your framework doesn't have something like this params then create class which wraps your framework's
        cookies system and allows to use the call chain obj.cookies.get() & cookies.delete()
        """
        session_id = request.cookies.get('session_id')
        if session_id is None:
            return
        response.delete_cookie('session_id')
        self.session_deleter.delete_session(session_id)