from .auth import router as auth_router
from .users import router as users_router
from .board import router as board_router

ROUTERS = [auth_router, users_router, board_router]
