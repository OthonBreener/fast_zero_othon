from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import UserPublic, UserSchema
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

router_users = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router_users.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def created_user(user: UserSchema, session: T_Session):
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


@router_users.get(
    '/', status_code=HTTPStatus.OK, response_model=list[UserPublic]
)
def read_users(session: T_Session):
    """
    limit: limita a quantidade de dados que vão ser retornados na busca.
    offset: define a partir de onde deve retornar os dados

    session.scalars(select(User).limit(2).offset(2)).all()
    """
    users = session.scalars(select(User)).all()

    return users


@router_users.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_by_id(user_id: int, session: T_Session):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return user


@router_users.put(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: CurrentUser,
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


@router_users.delete(
    '/{user_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only deleted your own user',
        )

    session.delete(current_user)
    session.commit()
