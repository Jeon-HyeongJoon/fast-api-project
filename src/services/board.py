from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.board import Board

class BoardCreate(BaseModel):
    title: str
    content: str

class BoardUpdate(BaseModel):
    title: str
    content: str

class BoardResponse(BaseModel):
    id: int
    title: str
    writer: str
    content: str

        
        
async def get_board(session: AsyncSession, board_id: int):
    result = await session.execute(select(BoardResponse).filter(BoardResponse.board_id == board_id))
    return result.scalars().first()

async def get_boards(session: AsyncSession, skip: int = 0, limit: int = 10):
    result = await session.execute(select(BoardResponse).offset(skip).limit(limit))
    return result.scalars().all()

async def create_board(session: AsyncSession, board: BoardCreate, user_id: int=1):
    db_board = Board(
        title=board.title,
        content=board.content,
        writer_id=user_id
    )
    session.add(db_board)
    await session.commit()
    await session.refresh(db_board)
    return db_board

async def update_board(session: AsyncSession, board_id: int, board: BoardUpdate):
    db_board = await get_board(session, board_id)
    if db_board:
        db_board.title = board.title
        db_board.content = board.content
        db_board.modified_at = func.current_timestamp()
        await session.commit()
        await session.refresh(db_board)
    return db_board

async def delete_board(session: AsyncSession, board_id: int):
    db_board = await get_board(session, board_id)
    if db_board:
        await session.delete(db_board)
        await session.commit()
    return db_board