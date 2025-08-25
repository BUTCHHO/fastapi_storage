from pytest import raises

from app.domain.value_objects.user.user_name.validation import validate_username_length, validate_name_pattern
from app.domain.value_objects.user.user_name.constants import USERNAME_MAX_LEN, USERNAME_MIN_MEN
from app.domain.exceptions.base import DomainFieldError
from app.domain.value_objects.user.user_name.user_name import UserName

def test_create_username():
    value = 'im_a_good_user'
    username = UserName(value)
    assert username.value == value

def test_create_username_incorrect():
    values = [
        '_i_am_a_bad_user',
        'a' * (USERNAME_MIN_MEN-1),
    ]
    with raises(DomainFieldError):
        for value in values:
            UserName(value)


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

def test_pattern_username_raises():
    with raises(DomainFieldError):
        validate_name_pattern('--_--_')

def tsst_pattern_username_correct_name():
    name = 'qwerty_123'
    validate_name_pattern(name)