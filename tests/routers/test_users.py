from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_created_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'user',
            'email': 'user@hotmail.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'user',
        'email': 'user@hotmail.com',
        'id': 1,
    }


def test_created_user_with_user_name_exists(client, user):
    user = user()

    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'user@hotmail.com.br',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_created_user_with_email_exists(client, user):
    user = user()

    response = client.post(
        '/users/',
        json={
            'username': 'user2',
            'email': user.email,
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client, user):
    user = user()

    response = client.get(
        '/users/',
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == [
        {'id': user.id, 'username': user.username, 'email': user.email}
    ]


def test_read_user_by_id(client, user):
    user = user()

    response = client.get(
        f'/users/{user.id}',
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_read_user_by_id_not_found(client, user):
    response = client.get(
        '/users/2',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    user = user()

    token = token(user)

    # transforma o model sqlal em um schema pydantic
    user_schema = UserPublic.model_validate(user).model_dump()

    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'teste atualizar',
            'email': 'user@hotmail.com.br',
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response_update.status_code == HTTPStatus.OK

    assert response_update.json() != user_schema


def test_update_user_with_id_invalid(client, user, token):
    token = token(user())

    user_2 = user()

    response = client.put(
        f'/users/{user_2.id}',
        json={
            'username': 'teste atualizar',
            'email': 'user@hotmail.com.br',
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    user = user()

    token = token(user)

    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    # Faço uma query para confirmar que não existe usuario no banco
    response = client.get(
        '/users/',
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == []


def test_delete_user_not_authorization(client, user):
    user = user()

    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': 'Bearer token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user_id_incorrect(client, user, token):
    token = token(user())

    user_2 = user()

    response = client.delete(
        f'/users/{user_2.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
