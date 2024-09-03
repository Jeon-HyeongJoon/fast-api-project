from fastapi import APIRouter
from src.services.auth import (
    User,
    CurrentUserDepends,
)
from typing import List
from src.modules.database import AsyncSessionDepends
from src.services.admin import User, get_all_users as admin_get_all_users
from src.modules.exceptions import AuthExceptions

router = APIRouter(prefix="/users")


@router.get("/me", response_model=User)
async def read_users_me(current_user: CurrentUserDepends):
    print(current_user)
    return current_user

# @router.post("/me", response_model=User)
# async def update_users_me(
#     update_user: UpdateForm
#     current_user: CurrentUserDepends
#     ) -> bool :
    
@router.get("/")
async def read_all_users(current_user: CurrentUserDepends,session: AsyncSessionDepends):
    if current_user.role != '0':
        raise AuthExceptions.CREDENTIALS_EXCEPTION
  
    return await admin_get_all_users(session)
