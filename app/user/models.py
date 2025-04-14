from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.core.database import DBBase


class User(DBBase):
    """
    Database model for users
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    pfp_url = Column(String, nullable=False, default="/avatar.png")
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)


class UserRefreshToken(DBBase):
    """
    Database model for user refresh tokens
    """

    __tablename__ = "user_refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
