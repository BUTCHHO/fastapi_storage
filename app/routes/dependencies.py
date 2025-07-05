from depends import AuthDepend
from app.routes.authorization.router import auth_handler

auth_depend = AuthDepend(auth_handler)
