from src.modules.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from datetime import datetime

from src.models.users import User
from src.models.board import Board

# CREATE TABLE Comments (
#     comment_id INT PRIMARY KEY AUTO_INCREMENT,
#     content TEXT NOT NULL,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     writer_id INT,
#     board_id INT,
#     parent_comment_id INT DEFAULT NULL,
#     FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL,
#     FOREIGN KEY (notice_id) REFERENCES Notices(notice_id) ON DELETE CASCADE,
#     FOREIGN KEY (parent_comment_id) REFERENCES Comments(comment_id) ON DELETE SET NULL
# );

class Comment(Base) :
    __tablename__ = "comments"
    
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    modified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    writer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    writer: Mapped[User] = relationship("User")
    board_id: Mapped[int] = mapped_column(Integer, ForeignKey("board.board_id", ondelete="CASCADE"), nullable=False)
    board: Mapped[Board] = relationship("Board")
    parent_comment_id: Mapped[int] = mapped_column(Integer, ForeignKey('comments.comment_id', ondelete="SET NULL"), nullable=True)
    parent_comment: Mapped['Comment'] = relationship("Comment", remote_side=[comment_id], backref="child_comments")
    
    def serialize(self):
        return dict(
                id=self.comment_id,
                writer=self.writer_id,
                content=self.content,
                created_at=self.created_at,
                modified_at=self.modified_at
                )