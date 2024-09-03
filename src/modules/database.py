from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config import secret_settings

Base = declarative_base()

database_url = URL(
    drivername="mysql+aiomysql",
    username=secret_settings.db_username,
    password=secret_settings.db_password,
    host=secret_settings.db_host,
    port=secret_settings.db_port,
    database=secret_settings.db_dbname,
    query={},
)



engine = create_async_engine(
    database_url,
    pool_recycle=300,
    pool_size=10,
    max_overflow=100,
)


SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def Session():
    async with SessionFactory() as async_session:
        yield async_session


async def database():
    async with Session() as s:
        yield s


AsyncSessionDepends = Annotated[AsyncSession, Depends(database)]
