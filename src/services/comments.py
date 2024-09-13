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
    parent_comment_id: Optional[int] = None

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    writer: int
    content: str
    created_at: datetime
    modified_at: Optional[datetime] = None
    child_comments: Optional[List] = None


# 댓글 생성
async def create_comment(
    session: AsyncSession,
    board_id: int, 
    comment_data: CommentCreate,
    user_id: int=1
):
    # 게시물이 존재하는지 확인
    board = await session.get(Board, board_id)
    must(board, HTTPException(status_code=404, detail="Board not found"))
    if comment_data.parent_comment_id:
        parents_comment = await session.get(Comment, comment_data.parent_comment_id)
        must(parents_comment.parent_comment_id is None, HTTPException(status_code=404, detail="can't create comment"))
    
    # 댓글 생성
    new_comment = Comment(
        content=comment_data.content,
        writer_id=user_id,
        board_id=board_id,
        parent_comment_id=comment_data.parent_comment_id,
    )
    
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    
    return new_comment.serialize()

async def get_child_comments(session: AsyncSession, comment_id: int) -> List[CommentResponse]:
    result = await session.execute(select(Comment).filter(Comment.parent_comment_id == comment_id))
    child_comments = result.scalars().all()

    return [CommentResponse(**comment.serialize())for comment in child_comments]
    
# 댓글 조회 (해당 게시물의 모든 댓글)
async def get_comments(
    session: AsyncSession,
    board_id: int,
    skip: int, 
    limit: int
):
    # 게시물이 존재하는지 확인
    board = await session.get(Board, board_id)
    must(board, HTTPException(status_code=404, detail="Board not found"))
    
    # 댓글 조회
    result = await session.execute(select(Comment).filter(
        Comment.board_id == board_id,
        Comment.parent_comment_id == None
    )).offset(skip).limit(limit)
    comments = result.scalars().all()
    
    # 부모 댓글에 대한 자식 댓글까지 포함하여 재귀적으로 반환
    return [
        CommentResponse(
            id=comment.comment_id,
            writer=comment.writer_id,
            content=comment.content,
            created_at=comment.created_at,
            modified_at=comment.modified_at,
            child_comments=await get_child_comments(session, comment.comment_id)
        )
        for comment in comments
    ]

# 댓글 수정
async def update_comment(
    session: AsyncSession,
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
async def delete_comment(
    session: AsyncSession,
    board_id: int, 
    comment_id: int
):
    # 댓글이 존재하는지 확인
    comment = await session.get(Comment, comment_id)
    must(comment, HTTPException(status_code=404, detail="Comment not found"))

    comment.content = "deleted"
    # await session.delete(comment)
    await session.commit()
    await session.refresh(comment)
    
    return True