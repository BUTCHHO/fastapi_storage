
class SettingsHandler:
    def __init__(self, acc_deleter, logger, user_logouter, storage_deleter):
        self.account_deleter = acc_deleter
        self.logger = logger
        self.logouter = user_logouter
        self.storage_deleter = storage_deleter

    def delete_storage(self, user_id):
        try:
            self.storage_deleter.delete_storage_by_user_id(user_id)
        except Exception as e:
            self.logger.log(e)

    def delete_account(self, user_id, should_delete, request, response):
        try:
            self.logouter.logout_user(request=request, response=response)
            self.account_deleter.delete_user_by_id(user_id)
            if should_delete:
                self.delete_storage(user_id)
        except Exception as e:
            self.logger.log(e)