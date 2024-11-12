from http import HTTPStatus

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, TodoState


def test_create_todo(client, user, token):
    user = user()
    token = token(user)

    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test description',
            'state': 'draft',
        },
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test description',
        'state': 'draft',
    }


def test_delete_todo(client, session, user, token, todos):
    user = user()
    token = token(user)

    todos(quantity=1)

    assert session.scalars(select(Todo)).all()

    response = client.delete(
        '/todos/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Todo deleted'}

    assert not session.scalars(select(Todo)).all()


def test_delete_todo_not_found(client, session, user, token, todos):
    user = user()
    token = token(user)

    todos(quantity=1)

    assert session.scalars(select(Todo)).all()

    response = client.delete(
        '/todos/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_todo(client, user, token, todos):
    user = user()
    token = token(user)

    todo = todos(quantity=1)[0]

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'test title',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'test title'


def test_patch_todo_not_found(client, user, token, todos):
    user = user()
    token = token(user)

    todos(quantity=1)

    response = client.patch(
        '/todos/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'test title',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    ('quantity', 'title', 'description', 'state'),
    [
        (5, 'Test title', '', None),
        (5, 'Test title', 'Test description', None),
        (5, 'Test title', 'Test description', 'done'),
        (5, '', 'Test description', None),
    ],
)
def test_list_todos(
    client,
    session,
    user,
    token,
    todos,
    quantity,
    title,
    description,
    state,
):
    user = user()
    token = token(user)

    # crio todos com os parametros passados
    todos(
        quantity=quantity,
        title=title,
        state=TodoState(state) if state else None,
        description=description,
    )

    if title and (description or state):
        todos(
            quantity=quantity,
            title=title,
        )

    # crio todos aleatorios para testar os filtros
    todos(quantity=quantity)

    # monto a query string para os filtros passados
    query = ''
    if title or description or state:
        if title:
            query += f'?title={title}&'

        if query and description:
            query += f'description={description}&'

        elif description:
            query += f'?description={description}&'

        if query and state:
            query += f'state={state}'

        elif state:
            query += f'?state={state}'

    # testar a rota de listagem de todos
    response = client.get(
        '/todos/' + query,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    todos_response = response.json().get('todos')

    assert todos_response
    assert len(todos_response) == quantity

    todos_db = session.scalars(select(Todo)).all()

    assert len(todos_db) > quantity

    for todo_response in todos_response:
        if title:
            assert todo_response['title'] == title

        if description:
            assert todo_response['description'] == description

        if state:
            assert todo_response['state'] == state
