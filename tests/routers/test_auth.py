from http import HTTPStatus


def test_login_for_access_token(client, user):
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
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
