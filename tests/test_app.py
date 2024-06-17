from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_read_root_deve_retornar_ok():
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
