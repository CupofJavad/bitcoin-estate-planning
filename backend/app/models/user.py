"""User model for authentication."""

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """User model extending FastAPI Users base table."""

    __tablename__ = "users"

    # Additional fields beyond FastAPI Users defaults
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # FastAPI Users provides:
    # - id (int, primary key)
    # - email (str, unique, indexed)
    # - hashed_password (str)
    # - is_active (bool, default=True)
    # - is_superuser (bool, default=False)
    # - is_verified (bool, default=False)

