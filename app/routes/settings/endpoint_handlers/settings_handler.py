
class SettingsHandler:
    def __init__(self, acc_deleter, logger, user_logouter):
        self.account_deleter = acc_deleter
        self.logger = logger
        self.logouter = user_logouter


    def delete_account(self, user_id, request, response):
        try:
            self.logouter.logout_user(request=request, response=response)
            self.account_deleter.delete_user_by_id(user_id)
        except Exception as e:
            self.logger.log(e)