from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.board import Board
from src.models.users import User
from datetime import datetime
from typing import Optional


class BoardCreate(BaseModel):
    title: str
    content: str

class BoardUpdate(BaseModel):
    title: str
    content: str

class BoardSimple(BaseModel):
    id: int
    title: str
    writer: str

class BoardDetail(BaseModel):
    id: int
    title: str
    writer: str
    content: str
    created_at: datetime

        
        
async def get_board(session: AsyncSession, board_id: int):
    # result = await session.execute(select(Board).filter(Board.board_id == board_id))
    # return result.scalars().first()
    result = await session.execute(select(Board).options(selectinload(Board.writer)))
    board = result.scalars().first()
    return BoardDetail(
                id=board.board_id, 
                title=board.title, 
                writer=board.writer.user_name, 
                content=board.content, 
                created_at=board.created_at
            )

async def get_boards(session: AsyncSession, skip: int = 0, limit: int = 10):
    result = await session.execute(select(Board).options(selectinload(Board.writer)).offset(skip).limit(limit))
    boards = result.scalars().all()
    return [BoardSimple(id=board.board_id, title=board.title, writer=board.writer.user_name) for board in boards]

async def create_board(session: AsyncSession, board: BoardCreate, user_id: int=1):
    new_board = Board(
        title=board.title,
        content=board.content,
        writer_id=user_id
    )
    session.add(new_board)
    await session.commit()
    await session.refresh(new_board)
    return new_board

async def update_board(session: AsyncSession, board_id: int, board: BoardUpdate):
    db_board = await session.get(Board, board_id)
    if db_board:
        db_board.title = board.title
        db_board.content = board.content
        db_board.modified_at = func.current_timestamp()
        await session.commit()
        await session.refresh(db_board)
    return db_board

async def delete_board(session: AsyncSession, board_id: int):
    db_board = await session.get(Board, board_id)
    if db_board:
        await session.delete(db_board)
        await session.commit()
        return True
    return False