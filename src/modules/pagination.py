from typing import Callable, Generic, TypeVar

from pydantic import BaseModel
from pydantic.v1.generics import GenericModel
from sqlalchemy import func, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class PaginationInput(BaseModel):
    page: int
    size: int


class PaginationResult(GenericModel, Generic[T]):
    total: int
    current: int
    size: int
    items: list[T]


async def pagination_builder(
    query: Select,
    session: AsyncSession,
    data: PaginationInput,
    mapper: Callable = lambda x: x,
) -> PaginationResult:
    total_q = select(func.count()).select_from(query.order_by(None).subquery())
    total = await session.scalar(total_q)
    offset = (data.page - 1) * data.size
    items_q = query.limit(data.size).offset(offset)
    items = (await session.scalars(items_q)).all()

    return PaginationResult(
        total=total,
        current=data.page,
        size=data.size,
        items=[mapper(i) for i in items],
    )
