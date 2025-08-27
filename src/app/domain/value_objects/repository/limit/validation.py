from app.domain.value_objects.repository.limit.constants import REPOSITORY_MAX_SIZE_BYTES
from app.domain.exceptions.base import DomainFieldError


def validate_limit_size(limit_value):
    if limit_value > REPOSITORY_MAX_SIZE_BYTES:
        raise DomainFieldError(f'Repository max size bytes must be less than {REPOSITORY_MAX_SIZE_BYTES}')