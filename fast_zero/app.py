from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token, UserPublic, UserSchema
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password_hash,
)

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

    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

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
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only update your own user',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)
    return current_user


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only deleted your own user',
        )

    session.delete(current_user)
    session.commit()


@app.post(
    '/token',
    status_code=HTTPStatus.OK,
    response_model=Token,
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password_hash(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    return {
        'access_token': create_access_token({'sub': user.email}),
        'token_type': 'Bearer',
    }
