from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.modules.pagination import PaginationInput, PaginationResult, pagination_builder

class User(BaseModel):
    user_id: int
    user_name: str
    real_name: str
    role : str
    
    model_config = ConfigDict(from_attributes=True)


async def get_all_users(
        session: AsyncSession, 
        data: Optional[PaginationInput] = None
    ) -> PaginationResult:
    if data is None :
        data = PaginationInput(page=1, size=10)
    
    query = select(models.User)
    return await pagination_builder(query, session, data, User.model_validate)
 