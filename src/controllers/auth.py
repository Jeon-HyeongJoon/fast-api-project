import uuid

from fastapi import APIRouter, Response, Cookie
from src.modules.cache import CacheDepends
from src.modules.database import AsyncSessionDepends
from src.modules.exceptions import AuthExceptions
from src.modules.utils import must
from src.services.auth import (
    Token,
    authenticate_user,
    create_access_token,
    LoginForm,
    SignupForm,
    signup,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_default_expire,
)
from starlette.responses import PlainTextResponse

router = APIRouter(prefix="/auth")



@router.post("/signup")
async def _router_signup(
    form: SignupForm,
    session: AsyncSessionDepends,
):
    new_user = await signup(session, form)
    await session.commit()

    # return new_user.user_id
    return new_user.serialize()


@router.post("/login")
async def _router_login(
    form: LoginForm,
    session: AsyncSessionDepends,
    cache: CacheDepends,
    response: Response,
) -> Token:
    user = await authenticate_user(session, form)
    must(user, AuthExceptions.INCORRECT_FORM)

    session_id = str(uuid.uuid4())
    await cache.set(
        name=session_id, ex=ACCESS_TOKEN_EXPIRE_MINUTES * 60, value=user.user_id
    )
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        expires=get_default_expire().isoformat(),
    )
    access_token = create_access_token(data={"sub": str(user.user_id)})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def _router_logout(
    cache: CacheDepends, 
    response: Response, session_id: str = Cookie(None)
):
    must(session_id, AuthExceptions.SESSION_NOT_FOUND)
    if await cache.exists(session_id):
        await cache.delete(session_id)
    else:
        raise AuthExceptions.SESSION_UNKNOWN

    response.delete_cookie(key="session_id")
    return {"message": "Logged out successfully"}
