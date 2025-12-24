"""User schemas for FastAPI Users."""

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """User read schema."""
    
    full_name: str | None = None


class UserCreate(schemas.BaseUserCreate):
    """User creation schema."""
    
    full_name: str | None = None


class UserUpdate(schemas.BaseUserUpdate):
    """User update schema."""
    
    full_name: str | None = None

