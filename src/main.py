from fastapi import APIRouter, FastAPI, Depends
from brotli_asgi import BrotliMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import PlainTextResponse

from src.controllers import ROUTERS
from src.modules.utils import get_environment
from src.services.request import RequestService

router = APIRouter()


@router.get("/", response_model=None)
async def hello(
    request: RequestService = Depends(),
):
    return PlainTextResponse(
        "Hello!\n"
        f"reserv-{get_environment()} is running\n"
        f"{request.base_url}\n"
        f"{request.user_agent}\n"
        f"{request.ip_address}\n"
        f"{request.browser}\n"
        f"{request.device}\n"
        f"{request.os}\n"
    )


def create_app():
    _app = FastAPI()
    _app.include_router(router)
    for _router in ROUTERS:
        _app.include_router(_router)
    return _app


app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BrotliMiddleware)
app.add_middleware(GZipMiddleware)
