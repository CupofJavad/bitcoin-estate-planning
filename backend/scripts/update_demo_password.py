"""Update demo user password."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.core.database import AsyncSessionLocal as async_session_maker
from app.models.user import User
import bcrypt


def hash_password(password: str) -> str:
    """Hash password using bcrypt directly."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


async def update_demo_password():
    """Update demo user password."""
    async with async_session_maker() as session:
        try:
            # Find demo user
            result = await session.execute(
                select(User).where(User.email == "demo@example.com")
            )
            user = result.scalar_one_or_none()
            
            if not user:
                print("❌ Demo user not found!")
                return
            
            # Update password
            new_password = "demo123456"
            hashed_password = hash_password(new_password)
            
            await session.execute(
                update(User)
                .where(User.email == "demo@example.com")
                .values(hashed_password=hashed_password)
            )
            await session.commit()
            
            print(f"✅ Password updated for {user.email}")
            print(f"   New password: {new_password}")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error updating password: {str(e)}")
            raise


if __name__ == "__main__":
    asyncio.run(update_demo_password())

