from datetime import datetime

from sqlalchemy import DateTime, Integer, func, String
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    # email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(60), nullable=False)
    real_name: Mapped[str] = mapped_column(String(128), nullable=False)
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
                real_name=self.real_name, 
                role=self.role
                )
