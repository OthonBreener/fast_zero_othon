from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='teste user', password='123456', email='teste_user@gmail.com'
    )

    assert user.id is None

    session.add(user)
    session.commit()

    session.refresh(user)

    assert user.id is not None

    user = session.query(User).filter_by(username='teste user').first()

    assert user.username == 'teste user'
