from .auth import router as auth_router
from .users import router as users_router

ROUTERS = [auth_router, users_router]
