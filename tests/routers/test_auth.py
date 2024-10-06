from datetime import datetime
from http import HTTPStatus

from freezegun import freeze_time


def test_login_for_access_token(client, user):
    user = user()

    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json().get('access_token') is not None
    assert response.json().get('token_type') == 'Bearer'


def test_login_for_access_token_invalid(client, user):
    user = user()

    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_expired_after_time(client, user):
    user = user()

    with freeze_time(datetime(2024, 1, 1, 17, 30)):
        response = client.post(
            '/auth/token',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json().get('access_token')

    with freeze_time(datetime(2024, 1, 1, 18, 1)):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'test',
                'email': 'test@test.com',
                'password': 'password',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert (
            response.json().get('detail') == 'Could not validate credentials'
        )


def test_refresh_access_token(client, user, token):
    user = user()

    token = token(user)

    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json().get('access_token') is not None
    assert response.json().get('token_type') == 'Bearer'


def test_token_expired_after_refresh(client, user, token):
    user = user()

    token = token(user)

    with freeze_time(datetime(2024, 1, 1, 17, 30)):
        response = client.post(
            '/auth/token',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json().get('access_token')

    with freeze_time(datetime(2024, 1, 1, 18, 1)):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert (
            response.json().get('detail') == 'Could not validate credentials'
        )
