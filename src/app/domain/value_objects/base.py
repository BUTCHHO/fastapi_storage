from dataclasses import dataclass, fields
from app.domain.exceptions.base import DomainFieldError


@dataclass
class ValueObject:
    def __post_init__(self):

        if not fields(self):
            raise DomainFieldError('Value object must have at least 1 field')