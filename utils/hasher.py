from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe

class Hasher:

    def generate_psw_hash(self, password):
        return generate_password_hash(password)

    def checK_password(self, password, hashed_psw):
        return check_password_hash(hashed_psw, password)

    def create_session_id_hash(self):
        return token_urlsafe(32)
