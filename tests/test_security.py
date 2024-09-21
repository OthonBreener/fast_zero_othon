import pytest
from jwt import decode

from fast_zero.security import (
    create_access_token,
    credentials_exception,
    get_current_user,
)
from fast_zero.settings import Settings


def test_create_access_token():
    data = {'sub': 'user'}

    token = create_access_token(data)

    assert token is not None

    decoded = decode(
        token, Settings().SECRETY_KEY, algorithms=[Settings().ALGORITHM]
    )

    assert list(decoded.keys()) == ['sub', 'exp']


def test_get_current_user(client, user, session):
    token = create_access_token({'sub': user.email})

    user = get_current_user(session, token)

    assert user is not None


def test_get_current_user_with_not_content(client, user, session):
    token = create_access_token({'sub': ''})

    with pytest.raises(
        Exception, match='Could not validate credentials'
    ) as exc_info:
        get_current_user(session, token)

    assert isinstance(exc_info.value, credentials_exception.__class__)
    assert exc_info.value.detail == 'Could not validate credentials'


def test_get_current_user_with_not_user(client, user, session):
    token = create_access_token({'sub': 'teste@hotmail.com'})

    with pytest.raises(
        Exception, match='Could not validate credentials'
    ) as exc_info:
        get_current_user(session, token)

    assert isinstance(exc_info.value, credentials_exception.__class__)
    assert exc_info.value.detail == 'Could not validate credentials'
