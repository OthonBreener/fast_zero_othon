from http import HTTPStatus


def test_read_root_deve_retornar_ok(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
