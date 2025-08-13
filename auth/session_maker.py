class SessionMaker:
    def __init__(self, session_reader, session_actor, time_handler, hasher, cacher, SESSION_EXPIRE_DAYS):
        self.session_reader = session_reader
        self.session_actor = session_actor
        self.hasher = hasher
        self.cacher = cacher
        self.time_handler = time_handler
        self.SESSION_EXPIRE_DAYS = SESSION_EXPIRE_DAYS

    async def _delete_session_if_already_exists(self, user_id):
        if session := await self.session_reader.get_by_kwargs(user_id=user_id):
            self.cacher.delete_data(session.id)
            await self.session_actor.delete_record_by_kwargs(user_id=user_id)

    def _make_session_obj(self, user_id):
        session_id = self.hasher.generate_session_id_hash()
        print(type(self.SESSION_EXPIRE_DAYS), 'TYPE OF SESSION EXPIRE DAYS', self.SESSION_EXPIRE_DAYS)
        session_expire_date = self.time_handler.add_days_to_current_date(self.SESSION_EXPIRE_DAYS)
        return self.session_actor.create_record(id=session_id, user_id=user_id, expire_date=session_expire_date)

    async def make_session_and_save(self, user_id):
        await self._delete_session_if_already_exists(user_id)
        session = self._make_session_obj(user_id)
        session_id = session.id
        await self.session_actor.write_record_to_db(record=session)
        self.cacher.put_data(session_id, user_id)
        return session_id
