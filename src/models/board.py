from src.modules.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func,ForeignKey
from datetime import datetime
 
from src.models.users import User
 
# CREATE TABLE Board (
#     board_id INT PRIMARY KEY AUTO_INCREMENT,
#     title VARCHAR(200) NOT NULL,
#     content TEXT NOT NULL,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     user_id INT,
#     FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL
# );

class Board(Base):
    __tablename__ = "board"
    
    board_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    modified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    writer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    writer: Mapped[User] = relationship("User")
    
    def serialize(self):
        return dict(
                id=self.board_id,
                title=self.title,
                writer=self.writer,
                content=self.content,
                created_at=self.created_at,
                modified_at=self.modified_at
                )