from interfaces import IModelActor


class SessionDeleter:
    def __init__(self, cacher, session_actor):
        self.cacher = cacher
        self.session_actor: IModelActor = session_actor

    def delete_session(self, session_id):
        """
        MAKE SURE YOU DELETE SESSION_ID FROM USER COOKIES!!!
        :param session_id:
        :return:
        """
        self.cacher.delete_data(session_id)
        self.session_actor.delete_record_by_id(session_id)