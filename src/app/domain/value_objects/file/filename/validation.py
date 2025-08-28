import re

from app.domain.value_objects.file.filename.constants import MAX_FILENAME_LENGTH, MIN_FILENAME_LENGTH, FILENAME_PATTERN

from app.domain.exceptions.base import DomainFieldError


def validate_filename_length(filename_value):
    if MIN_FILENAME_LENGTH > len(filename_value) > MAX_FILENAME_LENGTH:
        raise DomainFieldError(f'filename length must be between {MIN_FILENAME_LENGTH} - {MAX_FILENAME_LENGTH}')

def validate_filename_pattern(filename_value):
    if re.match(FILENAME_PATTERN, filename_value) == None:
        raise DomainFieldError(f'filename does not match to FILENAME_PATTERN')
