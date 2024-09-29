from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, func, String
from datetime import datetime

from src.modules.database import Base

# CREATE TABLE Users (
#     user_id INT PRIMARY KEY AUTO_INCREMENT,
#     username VARCHAR(50) NOT NULL,
#     email VARCHAR(100) NOT NULL UNIQUE,
#     password VARCHAR(255) NOT NULL,
#     role VARCHAR(20) DEFAULT 'user',  -- 사용자 역할 (예: 'user', 'admin')
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hashed_password: Mapped[str] = mapped_column(String(60), nullable=False)
    user_name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

    def serialize(self):
        return dict(
                id=self.user_id, 
                user_name=self.user_name, 
                email=self.email, 
                role=self.role
                )
