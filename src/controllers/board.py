from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.database import AsyncSessionDepends
from src.services.board import (
    BoardCreate, 
    BoardUpdate, 
    get_board, 
    get_boards, 
    create_board, 
    update_board, 
    delete_board,
    search_boards
)
from typing import List
from src.services.auth import CurrentUserDepends

router = APIRouter(prefix="/board")

# 게시물 생성
@router.post("/")
async def _router_create_new_board(
    session: AsyncSessionDepends, 
    board: BoardCreate, 
    # user: CurrentUserDepends
):
    return await create_board(session=session, board=board, user_id=1)

# 특정 게시물 조회
@router.get("/{board_id}")
async def _router_read_board(
    session: AsyncSessionDepends,
    board_id: int
):
   return await get_board(session, board_id=board_id)

# 전체 게시물 목록 조회
# @router.get("/")
# async def _router_read_boards(
#     session: AsyncSessionDepends,
#     skip: int = 0, 
#     limit: int = 10
# ):
#     return await get_boards(session, skip=skip, limit=limit)

# 게시물 검색 및 전체 게시물 목록 조회
@router.get("/")
async def _router_search_boards(
    session: AsyncSessionDepends,
    search: str = "",
    skip: int = 0,
    limit: int = 10
):
    return await search_boards(session, search=search, skip=skip, limit=limit)

# 게시물 수정
@router.put("/{board_id}")
async def _router_update_board_item(
    session: AsyncSessionDepends, 
    board: BoardUpdate, 
    board_id: int
):
    return await update_board(session, board_id=board_id, board=board)

# 게시물 삭제
@router.delete("/{board_id}")
async def _router_delete_board_item(
    session: AsyncSessionDepends,
    board_id: int
):
    await delete_board(session, board_id=board_id)
    return {"message": "Board deleted successfully"}

