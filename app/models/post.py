from datetime import datetime
from sqlalchemy import (
    Column, 
    Integer,
    Text, 
    String, 
    Boolean, 
    DateTime,
    func
)
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

# class Post(Base):
#     __tablename__ = "posts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     title: Mapped[str] = mapped_column(String(200), nullable=False)
#     content: Mapped[str] = mapped_column(Text, nullable=False)
#     is_published: Mapped[bool] = mapped_column(Boolean, server_default="false")
#     created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Post(Base):
    __tablename__ = "articles"  # <-- 1. Renamed table
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)  # <-- 2. Renamed content to body
    views: Mapped[int] = mapped_column(Integer, server_default="0")  # <-- 3. Added new column
    is_published: Mapped[bool] = mapped_column(Boolean, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())