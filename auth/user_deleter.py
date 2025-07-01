from interfaces import IModelActor


class UserDeleter:
    def __init__(self, user_actor):
        self.user_actor: IModelActor = user_actor

    def delete_user_by_id(self, user_id):
        #make sure to delete session_id from user's cookies and from db
        self.user_actor.delete_record_by_id(user_id)