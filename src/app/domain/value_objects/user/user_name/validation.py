import re

from app.domain.value_objects.user.user_name.constants import (USERNAME_MAX_LEN,
                                                               USERNAME_MIN_MEN,
                                                               PATTERN_END,
                                                               PATTERN_NO_CONSECUTIVE_SPECIALS,
                                                               PATTERN_ALLOWED_CHARS,
                                                               PATTERN_START,

                                                               )
from app.domain.exceptions.base import DomainFieldError


def validate_username_length(name:str):
    if not USERNAME_MIN_MEN < len(name) < USERNAME_MAX_LEN:
        raise DomainFieldError(f'Username len must be between {USERNAME_MIN_MEN} and {USERNAME_MAX_LEN}!')

