from app.domain.value_objects.repository.name.constants import (REPONAME_MAX_LEN,REPONAME_MIN_LEN,
                                                                PATTERN_END,PATTERN_START,
                                                                PATTERN_ALLOWED_CHARS, PATTERN_NO_CONSECUTIVE_SPECIALS
                                                                )
from app.domain.exceptions.base import DomainFieldError
import re


def validate_name_length(reponame_value:str):
    if not REPONAME_MIN_LEN < len(reponame_value) < REPONAME_MAX_LEN:
        raise DomainFieldError(f'Reponame len must be between {REPONAME_MIN_LEN} and {REPONAME_MAX_LEN}!')

def validate_name_pattern(reponame_value:str):
    if not re.match(PATTERN_START, reponame_value):
        raise DomainFieldError(
            "Reponame must start with a letter (A-Z, a-z) or a digit (0-9).",
        )
    if not re.fullmatch(PATTERN_ALLOWED_CHARS, reponame_value):
        raise DomainFieldError(
            "Reponame can only contain letters (A-Z, a-z), digits (0-9), "
            "dots (.), hyphens (-), and underscores (_).",
        )
    if not re.fullmatch(PATTERN_NO_CONSECUTIVE_SPECIALS, reponame_value):
        raise DomainFieldError(
            "Reponame cannot contain consecutive special characters"
            " like .., --, or __.",
        )
    if not re.match(PATTERN_END, reponame_value):
        raise DomainFieldError(
            "Reponame must end with a letter (A-Z, a-z) or a digit (0-9).",
        )