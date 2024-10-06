from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import (
    create_access_token,
    get_current_user,
    verify_password_hash,
)

router_auth = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]


@router_auth.post(
    '/token',
    status_code=HTTPStatus.OK,
    response_model=Token,
)
def login_for_access_token(
    form_data: OAuth2Form,
    session: T_Session,
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


@router_auth.post(
    '/refresh_token',
    response_model=Token,
)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_token = create_access_token({'sub': user.email})

    return {
        'access_token': new_token,
        'token_type': 'Bearer',
    }
