from auth.exceptions import SessionDontExists


class SessionGetter:
    def __init__(self, session_reader, cacher, session_validator, session_deleter):
        self.session_reader = session_reader
        self.cacher = cacher
        self.session_validator = session_validator
        self.session_deleter = session_deleter

    async def get_session_from_db(self, user_id):
        return await self.session_reader.get_by_kwargs(user_id=user_id)

    async def get_session_id_by_user_id(self, user_id):
        session = await self.get_session_from_db(user_id)
        if session is None:
            raise SessionDontExists
        await self.session_validator.validate_session_or_raise(session)
        return session
