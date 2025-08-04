from .exceptions import InvalidPassword, UserDontExists


class Authenticator:
    def __init__(self, user_getter, hasher, session_maker, session_reader, cacher):
        self.user_getter = user_getter
        self.hasher = hasher
        self.session_maker = session_maker
        self.session_reader = session_reader
        self.cacher = cacher

    async def auth_by_session_id(self, session_id):
        return await self.user_getter.get_by_session_id(session_id)


    async def auth_by_name_and_psw_and_return_session(self, name, psw):
        user = await self.user_getter.get_by_name(name)
        if user is None:
            raise UserDontExists
        if not self.hasher.compare_password_hashes(psw, user.password):
            raise InvalidPassword
        session = await self.session_maker.make_session_and_save(user.id)
        return session