from .auth import auth_handler
from depends import AuthDepend

auth_depend = AuthDepend(auth_handler)
