from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK


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
    response = client.post(
        '/users/',
        json={
            'username': 'user',
            'email': 'user@hotmail.com.br',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_created_user_with_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'user2',
            'email': 'user@hotmail.com.br',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client, user):
    response = client.get(
        '/users/',
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == [
        {'username': 'user', 'email': 'user@hotmail.com.br', 'id': 1}
    ]


def test_read_user_by_id(client, user):
    response = client.get(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'username': 'user',
        'email': 'user@hotmail.com.br',
        'id': 1,
    }


def test_read_user_by_id_not_found(client, user):
    response = client.get(
        '/users/2',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    # transforma o model sqlal em um schema pydantic
    user_schema = UserPublic.model_validate(user).model_dump()

    response_update = client.put(
        '/users/1',
        json={
            'username': 'teste atualizar',
            'email': 'user@hotmail.com.br',
            'password': 'password',
        },
    )

    assert response_update.status_code == HTTPStatus.OK

    assert response_update.json() != user_schema


def test_delete_user(client, user):
    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    # Faço uma query para confirmar que não existe usuario no banco
    response = client.get(
        '/users/',
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == []
