from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import BaseModel
from passlib.context import CryptContext

from diffsyncer import config


class Token(BaseModel):
    token: str
    type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_user(username: str, password: str):
    if username != "admin":
        return False

    if not verify_password(password, config.ADMIN_PASSWORD):
        return False

    return User(username=username)


def create_access_token(data: dict, expires: int = config.ACCESS_TOKEN_EXPIRE_SECONDS):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "expires": expires,
    }


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return credentials_exception

        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception

    # for security reasons, we should check if the user exists in the database
    # TODO: implement this part

    return User(username=token_data.username)
