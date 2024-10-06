from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.settings import Settings

pwd_context = PasswordHash.recommended()


credentials_exception = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expires = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expires})

    return encode(
        to_encode, Settings().SECRETY_KEY, algorithm=Settings().ALGORITHM
    )


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(OAuth2PasswordBearer(tokenUrl='/auth/token')),
) -> User:
    try:
        decoded = decode(
            token, Settings().SECRETY_KEY, algorithms=[Settings().ALGORITHM]
        )

        email = decoded.get('sub')
        if not email:
            raise credentials_exception

    except PyJWTError as e:
        raise credentials_exception from e
    except ExpiredSignatureError as e:
        raise credentials_exception from e

    user = session.scalar(select(User).where(User.email == email))

    if not user:
        raise credentials_exception

    return user
