from exceptions import APIUserAlreadyExists, UserAlreadyExists


class SignUpHandler:
    def __init__(self, user_registrator):
        self.user_registrator = user_registrator

    def sign_up(self, params):
        try:
            self.user_registrator.create_user(params.name, params.password)
        except UserAlreadyExists:
            raise APIUserAlreadyExists(params.name)