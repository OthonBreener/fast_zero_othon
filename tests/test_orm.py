from sqlalchemy import select

from fast_zero.models import Todo, User


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


def test_create_todo(session, user):
    user = user()

    todo = Todo(
        title='Test todo',
        description='Test description',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
