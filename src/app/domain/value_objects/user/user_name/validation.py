import re

from app.domain.value_objects.user.user_name.constants import (USERNAME_MAX_LEN,
                                                               USERNAME_MIN_MEN,
                                                               PATTERN_END,
                                                               PATTERN_NO_CONSECUTIVE_SPECIALS,
                                                               PATTERN_ALLOWED_CHARS,
                                                               PATTERN_START,

                                                               )
from app.domain.exceptions.base import DomainFieldError


def validate_username_length(username_value:str):
    if not USERNAME_MIN_MEN < len(username_value) < USERNAME_MAX_LEN:
        raise DomainFieldError(f'Username len must be between {USERNAME_MIN_MEN} and {USERNAME_MAX_LEN}!')

def validate_name_pattern(username_value:str):
    if not re.match(PATTERN_START, username_value):
        raise DomainFieldError(
            "Username must start with a letter (A-Z, a-z) or a digit (0-9).",
        )
    if not re.fullmatch(PATTERN_ALLOWED_CHARS, username_value):
        raise DomainFieldError(
            "Username can only contain letters (A-Z, a-z), digits (0-9), "
            "dots (.), hyphens (-), and underscores (_).",
        )
    if not re.fullmatch(PATTERN_NO_CONSECUTIVE_SPECIALS, username_value):
        raise DomainFieldError(
            "Username cannot contain consecutive special characters"
            " like .., --, or __.",
        )
    if not re.match(PATTERN_END, username_value):
        raise DomainFieldError(
            "Username must end with a letter (A-Z, a-z) or a digit (0-9).",
        )