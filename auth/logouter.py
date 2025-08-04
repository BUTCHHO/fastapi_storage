from .exceptions import SessionDontExists


class Logouter:
    def __init__(self, user_reader, session_reader, session_actor, cacher):
        self.user_reader = user_reader
        self.session_reader = session_reader
        self.session_actor = session_actor
        self.cacher = cacher

    async def delete_session_for_user(self, user_id):
        """
        :raises: SessionDontExists
        """
        session = await self.session_reader.get_by_kwargs(user_id=user_id)
        if session is None:
            raise SessionDontExists
        await self.session_actor.delete_record_by_kwargs(id=session.id)
        self.cacher.delete_data(session.id)