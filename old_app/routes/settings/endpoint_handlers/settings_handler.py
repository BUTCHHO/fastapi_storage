from fastapi import Request, Response

class SettingsHandler:
    def __init__(self, user_actor, user_logouter, storage_deleter):
        self.user_actor = user_actor
        self.logouter = user_logouter
        self.storage_deleter = storage_deleter

    def delete_storage(self, user_id):
        self.storage_deleter.delete_storage_by_user_id(user_id)


    async def delete_account(self, user_id, should_delete_storage, request: Request, response: Response):
        session_id = request.cookies.get('session_id')
        response.delete_cookie('session_id')
        await self.logouter.delete_session(session_id)
        await self.user_actor.delete_record_by_kwargs(id=user_id)
        if should_delete_storage:
            self.delete_storage(user_id)
