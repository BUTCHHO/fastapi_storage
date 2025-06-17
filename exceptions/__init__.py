from .path_http_exc import APIPathGoesBeyondLimits, APIEntityDoesNotExists, APIUnsupportedEntityType
from .exc import StoragePathIsNone, NotAUserId, DatabaseUrlIsNone
from .auth import UserAlreadyExists, UserDontExists, IncorrectPassword, SessionExpired
from .auth_http_exc import APIUserAlreadyExists