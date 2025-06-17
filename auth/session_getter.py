class SessionGetter:
    def __init__(self, db_reader):
        self.reader = db_reader


    def get_session_by_user_id(self, user_id):
        return self.reader.get_record_by(user_id=user_id)

    def get_session_by_id(self, id):
        return self.reader.get_record_by_id(id)