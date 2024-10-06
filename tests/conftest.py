import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session, table_registry
from fast_zero.models import User
from fast_zero.security import get_password_hash
from tests.factories import UserFactory


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        # Especificos para o sqlite
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    def make_user():
        password = 'password'

        user = UserFactory(
            password=get_password_hash(password),
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        user.clean_password = password

        return user

    return make_user


@pytest.fixture()
def token(client, user):
    def make_token(user_database: User | None = None):
        if not user_database:
            user_database = user()

        response = client.post(
            '/auth/token',
            data={
                'username': user_database.email,
                'password': user_database.clean_password,
            },
        )

        return response.json()['access_token']

    return make_token
