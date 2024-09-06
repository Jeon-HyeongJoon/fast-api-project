from fastapi import APIRouter, Depends, HTTPException
from src.modules.database import AsyncSessionDepends
from src.services.board import (
    BoardCreate, 
    BoardUpdate, 
    BoardResponse,
    get_board, 
    get_boards, 
    create_board, 
    update_board, 
    delete_board
)
from typing import List

router = APIRouter(prefix="/board")

# 게시물 생성
@router.post("/", response_model=BoardResponse)
async def create_new_board(
    session: AsyncSessionDepends, 
    board: BoardCreate, 
    user_id: int=1
):
    return await create_board(session=session, board=board, user_id=user_id)

# 특정 게시물 조회
@router.get("/{board_id}", response_model=BoardResponse)
async def read_board(
    session: AsyncSessionDepends,
    board_id: int
):
    db_board = await get_board(session, board_id=board_id)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board

# 전체 게시물 목록 조회
@router.get("/", response_model=List[BoardResponse])
async def read_boards(
    session: AsyncSessionDepends,
    skip: int = 0, 
    limit: int = 10
):
    return await get_boards(session, skip=skip, limit=limit)

# 게시물 수정
@router.put("/{board_id}", response_model=BoardResponse)
async def update_board_item(
    session: AsyncSessionDepends,
    board: BoardUpdate,
    board_id: int
):
    db_board = await update_board(session, board_id=board_id, board=board)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board

# 게시물 삭제
@router.delete("/{board_id}")
async def delete_board_item(
    session: AsyncSessionDepends,
    board_id: int
):
    db_board = await delete_board(session, board_id=board_id)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return {"message": "Board deleted successfully"}