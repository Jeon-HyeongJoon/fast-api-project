from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Annotated

from jose import jwt, JWTError
# from passlib.context import CryptContext
import bcrypt
from pydantic import BaseModel, EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.config import secret_settings
from src.modules.cache import CacheDepends
from src.modules.database import AsyncSessionDepends
from src.modules.exceptions import AuthExceptions
from src.modules.utils import must

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    user_name: str
    email: str
    role : str

class SignupForm(BaseModel):
    user_name: str
    email: EmailStr
    password: str

class LoginForm(BaseModel):
    email: EmailStr
    password: str


oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
TokenDepends = Annotated[str, Depends(oauth2_schema)]


def get_default_expire():
    return datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def hash_password(password: str):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def verify_password(origin: str, hashed: str) -> bool:
    origin_byte_enc = origin.encode('utf-8')
    hashed_byte_enc = hashed.encode('utf-8')
    return bcrypt.checkpw(password = origin_byte_enc , hashed_password = hashed_byte_enc)
    

# async def get_user_by_email(session: AsyncSession, email: str) -> models.User | None:
#     return await session.scalar(select(models.User).where(models.User.email == email))


# async def is_usable_email_or_raise(session: AsyncSession, email: str):
#     is_exist = bool(
#         await session.scalar(
#             select(func.count(models.User.user_id)).where(models.User.email == email)
#         )
#     )
#     must(not is_exist, AuthExceptions.EMAIL_EXISTS)
    
async def get_user_by_id(session: AsyncSession, id: int) -> models.User | None:
    return await session.scalar(select(models.User).where(models.User.user_id == id))


async def get_user_by_name(session: AsyncSession, user_name: str) -> models.User | None:
    return await session.scalar(select(models.User).where(models.User.user_name == user_name))


async def is_usable_id_or_raise(session: AsyncSession, user_name: str):
    is_exist = bool(
        await session.scalar(
            select(func.count(models.User.user_id)).where(models.User.user_name == user_name)
        )
    )
    must(not is_exist, AuthExceptions.USER_NAME_EXISTS)


async def signup(session: AsyncSession, data: SignupForm):
    await is_usable_id_or_raise(session, data.user_name)
    # await is_usable_email_or_raise(session, data.email)
    must(
        data.user_name and 0 < len(data.user_name) < 128,
        AuthExceptions.INVALID_FULLNAME_LENGTH,
    )
    must(
        data.email and 0 < len(data.email) < 128,
        AuthExceptions.INVALID_FULLNAME_LENGTH,
    )
    must(
        data.password and 8 < len(data.password),
        AuthExceptions.INVALID_PASSWORD_LENGTH,
    )

    user = models.User(
        user_name=data.user_name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role='0'
    )
    session.add(user)
    await session.flush([user])
    return user


async def authenticate_user(session: AsyncSession, data: LoginForm):
    user = await get_user_by_name(session, data.user_name)
    if not user:
        return False
    if not verify_password(data.password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = get_default_expire()

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret_settings.jwt_secret_key, algorithm=ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    session: AsyncSessionDepends,
    cache: CacheDepends,
    token: TokenDepends,
    session_id: str = Cookie(None),
) -> User:
    # if session is expired, raise credential exception
    must(session_id, AuthExceptions.SESSION_NOT_FOUND)
    must(await cache.exists(session_id), AuthExceptions.SESSION_UNKNOWN)
    
    try:
        payload = jwt.decode(
            token=token, key=secret_settings.jwt_secret_key, algorithms=[ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        must(user_id, AuthExceptions.CREDENTIALS_EXCEPTION)

    except JWTError:
        raise AuthExceptions.CREDENTIALS_EXCEPTION
    except Exception as e:
        raise e

    user = await session.get(models.User, user_id)
    must(user, AuthExceptions.CREDENTIALS_EXCEPTION)
    return User(**user.serialize())


CurrentUserDepends = Annotated[models.User, Depends(get_current_user)]