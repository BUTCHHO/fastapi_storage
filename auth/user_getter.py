from .exceptions import UserDontExists, SessionDontExists, SessionExpired


class UserGetter:
    def __init__(self, user_reader, session_reader, cacher, time_handler):
        self.user_reader = user_reader
        self.session_reader = session_reader
        self.cacher = cacher
        self.time_handler = time_handler

    async def get_by_session_id(self, session_id):
        user_id = self.cacher.get_data(session_id)
        if user_id is not None:
            return self.get_user_if_in_cache(user_id)
        session = await self.session_reader.get_by_kwargs(id=session_id)
        await self._raise_and_delete_session_if_invalid(session)
        user = await self.user_reader.get_by_kwargs(id=session.user_id)
        if not user:
            raise UserDontExists(user_id)
        return user

    async def get_user_if_in_cache(self, user_id):
        user = await self.user_reader.get_by_kwargs(id=user_id)
        if not user:
            raise UserDontExists(user_id)
        return user

    async def _raise_and_delete_session_if_invalid(self, session):
        if not session:
            raise SessionDontExists
        if not self.time_handler.is_date_future(session.expire_date):
            self.cacher.delete_data(session.id)
            await self.session_reader.delete_by_kwargs(id=session.id)
            raise SessionExpired(session.id)

    async def get_by_name(self, name):
        user = await self.user_reader.get_by_kwargs(name=name)
        if not user:
            raise UserDontExists()
        return user