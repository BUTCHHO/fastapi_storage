from interfaces import IModelActor
from interfaces import IModelReader

class SessionDeleter:
    def __init__(self, cacher, session_actor, session_reader):
        self.cacher = cacher
        self.session_actor: IModelActor = session_actor
        self.session_reader: IModelReader = session_reader

    def delete_session_by_user_id(self, user_id:str):
        session = self.session_reader.get_by_kwargs(user_id=user_id)
        self.delete_session(session.id)

    async def delete_session(self, session):
        """
        MAKE SURE YOU DELETE SESSION_ID FROM USER COOKIES!!!
        """
        self.cacher.delete_data(session.id)
        await self.session_actor.delete_record_by_id(id=session.id)