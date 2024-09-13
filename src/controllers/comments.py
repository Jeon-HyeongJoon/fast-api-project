from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from typing import List

from src.modules.database import AsyncSessionDepends
from src.models.board import Board
from src.models.comments import Comment
from src.services.comments import (
    CommentCreate, 
    CommentUpdate, 
    CommentResponse,
    create_comment,
    get_comments,
    update_comment,
    delete_comment
)

from src.modules.utils import must
from datetime import datetime

router = APIRouter()

# 댓글 생성
@router.post("/board/{board_id}/comments", response_model=CommentResponse)
async def _router_create_comment(
    session: AsyncSessionDepends,
    board_id: int, 
    comment_data: CommentCreate
):
    
    result = await create_comment(session, board_id, comment_data)
    must(result, HTTPException(status_code=404, detail="comment not found"))
    return result.serialize()

# 댓글 조회 (해당 게시물의 모든 댓글)
@router.get("/board/{board_id}/comments", response_model=List[CommentResponse])
async def _router_get_comments(
    session: AsyncSessionDepends,
    board_id: int
):

    result = await get_comments(session, board_id)
    must(result, HTTPException(status_code=404, detail="comment not found"))
    return result

# 댓글 수정
@router.put("/board/{board_id}/comments/{comment_id}", response_model=CommentResponse)
async def _router_update_comment(
    session: AsyncSessionDepends,
    board_id: int, 
    comment_id: int, 
    comment_data: CommentUpdate
):
    result = await update_comment(session, comment_id, comment_data)
    must(result, HTTPException(status_code=404, detail="comment not found"))
    return result.serialize()

# 댓글 삭제
@router.delete("/board/{board_id}/comments/{comment_id}", response_model=dict)
async def _router_delete_comment(
    session: AsyncSessionDepends,
    board_id: int, 
    comment_id: int
):
    # 댓글이 존재하는지 확인
    delete_success = await delete_comment(session, board_id, comment_id)
    if delete_success:
        return {"detail": "Comment deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="fail")