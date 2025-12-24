"""User model for authentication."""

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """User model extending FastAPI Users base table."""

    __tablename__ = "users"

    # Primary key (required - SQLAlchemyBaseUserTable doesn't define it in the actual table)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Additional fields beyond FastAPI Users defaults
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # FastAPI Users provides (via SQLAlchemyBaseUserTable):
    # - email: Mapped[str] (unique, indexed)
    # - hashed_password: Mapped[str]
    # - is_active: Mapped[bool] (default=True)
    # - is_superuser: Mapped[bool] (default=False)
    # - is_verified: Mapped[bool] (default=False)

