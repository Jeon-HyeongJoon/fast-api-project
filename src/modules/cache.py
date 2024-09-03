from typing import Annotated
from redis.asyncio import Redis, ConnectionPool
from fastapi import Depends

from src.config import secret_settings

redis_url = f"redis://{secret_settings.redis_host}:{secret_settings.redis_port}"
pool = ConnectionPool.from_url(redis_url)


async def get_cache():
    cache = Redis.from_pool(pool)
    try:
        yield cache
    finally:
        await cache.close()


CacheDepends = Annotated[Redis, Depends(get_cache)]
