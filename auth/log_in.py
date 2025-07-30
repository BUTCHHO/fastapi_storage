from auth.exceptions import UserDontExists, IncorrectPassword


class Login:
    def __init__(self, logger, hasher, user_access, session_access, session_maker):
        self.logger = logger
        self.user_access = user_access
        self.session_access = session_access
        self.hasher = hasher
        self.session_maker = session_maker

    def get_user(self, name):
        orig_user = self.user_access.get_by_kwargs(name=name)
        if orig_user is None:
            raise UserDontExists
        return orig_user

    def check_password(self, password, orig_password):
        if not self.hasher.check_password(password, orig_password):
            raise IncorrectPassword

    def make_session_and_get_id(self):
        session = self.session_maker.make_session()
        return session.id

    def login_user_by_password_and_get_session_id(self, name, password):
        """

        :param name:
        :param password:
        :return: session_id
        :raises: IncorrectPassword
        """
        orig_user = self.get_user(name)
        self.check_password(password, orig_user.password)
        session_id = self.make_session_and_get_id()
        return session_id