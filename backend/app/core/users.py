"""FastAPI Users configuration."""

from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User


# JWT Authentication Strategy
def get_jwt_strategy() -> JWTStrategy:
    """Get JWT authentication strategy."""
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# Bearer Transport (for JWT tokens)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Authentication Backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


# User Database
async def get_user_db(session: AsyncSession = Depends(get_db)) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """Get user database session."""
    yield SQLAlchemyUserDatabase(session, User)


# User Manager
class UserManager(BaseUserManager[User, int]):
    """User manager for FastAPI Users."""
    
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY
    
    def parse_id(self, value: str) -> int:
        """Parse user ID from string."""
        return int(value)
    
    async def on_after_register(self, user: User, request=None):
        """Called after user registration."""
        print(f"User {user.id} has registered.")
    
    async def on_after_forgot_password(self, user: User, token: str, request=None):
        """Called after forgot password request."""
        print(f"User {user.id} has requested password reset. Token: {token}")
    
    async def on_after_request_verify(self, user: User, token: str, request=None):
        """Called after verification request."""
        print(f"User {user.id} has requested verification. Token: {token}")


# User Manager Dependency
async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) -> AsyncGenerator[UserManager, None]:
    """Get user manager."""
    yield UserManager(user_db)


# FastAPI Users instance
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Current user dependency
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
