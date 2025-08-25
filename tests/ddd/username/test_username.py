from pytest import raises

from app.domain.value_objects.user.user_name.validation import validate_username_length
from app.domain.value_objects.user.user_name.constants import USERNAME_MAX_LEN, USERNAME_MIN_MEN
from app.domain.exceptions.base import DomainFieldError


def test_validate_name_length():
    name = 'a' * (USERNAME_MAX_LEN - 1)
    validate_username_length(name)

def test_validate_name_length_less_than_min():
    name = 'a' * (USERNAME_MIN_MEN - 1)
    with raises(DomainFieldError):
        validate_username_length(name)

def test_validate_name_length_more_than_max():
    name = 'a' * (USERNAME_MAX_LEN + 1)
    with raises(DomainFieldError):
        validate_username_length(name)
