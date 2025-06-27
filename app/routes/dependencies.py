from app.routes.authorization.router import auth_handler
from depends import AuthDepend

auth_depend = AuthDepend(auth_handler)
