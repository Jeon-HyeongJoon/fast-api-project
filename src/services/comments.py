from pydantic import BaseModel
from typing import Optional
from datetime import datetime


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.modules.database import AsyncSessionDepends
from src.models.board import Board
from src.models.comments import Comment

from src.modules.utils import must



class CommentCreate(BaseModel):
    content: str
    writer_id: int
    parent_comment_id: Optional[int] = None

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    writer: int
    content: str
    created_at: datetime
    modified_at: Optional[datetime] = None


# 댓글 생성
async def create_comment(
    session: AsyncSession,
    board_id: int, 
    comment_data: CommentCreate
):
    # 게시물이 존재하는지 확인
    board = await session.get(Board, board_id)
    must(board, HTTPException(status_code=404, detail="Board not found"))
    
    # 댓글 생성
    new_comment = Comment(
        content=comment_data.content,
        writer_id=comment_data.writer_id,
        board_id=board_id,
        parent_comment_id=comment_data.parent_comment_id,
        # created_at=func.current_timestamp()
    )
    
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    
    return new_comment.serialize()

# 댓글 조회 (해당 게시물의 모든 댓글)
@router.get("/board/{board_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    session: AsyncSessionDepends,
    board_id: int
):
    # 게시물이 존재하는지 확인
    board = await session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # 댓글 조회
    result = await session.execute(select(Comment).filter(Comment.board_id == board_id))
    comments = result.scalars().all()
    return [comment.serialize() for comment in comments]

# 댓글 수정
@router.put("/board/{board_id}/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    session: AsyncSessionDepends,
    board_id: int, 
    comment_id: int, 
    comment_data: CommentUpdate
):
    # 댓글이 존재하는지 확인
    comment = await session.get(Comment, comment_id)
    must(comment, HTTPException(status_code=404, detail="Comment not found"))

    # 댓글 수정
    comment.content = comment_data.content
    comment.modified_at = func.current_timestamp()
    
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    return comment.serialize()

# 댓글 삭제
@router.delete("/board/{board_id}/comments/{comment_id}", response_model=dict)
async def delete_comment(board_id: int, comment_id: int, session: AsyncSessionDepends):
    # 댓글이 존재하는지 확인
    comment = await session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    await session.delete(comment)
    await session.commit()
    
    return {"detail": "Comment deleted successfully"}