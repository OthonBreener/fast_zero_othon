from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import UserPublic, UserSchema

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root():
    html = """
    <html>
        <head>
            <title>Fast Zero</title>
        </head>
        <body>
            <h1>Hello World</h1>
            <p>Fast Zero</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def created_user(user: UserSchema, session: Session = Depends(get_session)):
    user_exists = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if user_exists:
        if user_exists.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )

        if user_exists.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=list[UserPublic])
def read_users(session: Session = Depends(get_session)):
    """
    limit: limita a quantidade de dados que vão ser retornados na busca.
    offset: define a partir de onde deve retornar os dados

    session.scalars(select(User).limit(2).offset(2)).all()
    """
    users = session.scalars(select(User)).all()

    return users


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return user


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    original_user = session.scalar(select(User).where(User.id == user_id))
    if not original_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    original_user.username = user.username
    original_user.email = user.email
    original_user.password = user.password
    session.commit()
    session.refresh(original_user)
    return original_user


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    session.delete(user)
    session.commit()
