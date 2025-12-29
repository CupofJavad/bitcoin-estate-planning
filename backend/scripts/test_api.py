"""Test API endpoint directly."""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.estate_plan import EstatePlan
from sqlalchemy import select
from app.api.v1.endpoints.estate_plans import get_demo_user

async def test():
    async with AsyncSessionLocal() as db:
        try:
            user = await get_demo_user(db=db)
            print(f"Demo user: {user.email} (ID: {user.id})")
            
            # Check estate plans
            result = await db.execute(
                select(EstatePlan).where(EstatePlan.user_id == user.id)
            )
            plans = result.scalars().all()
            print(f"Estate plans for {user.email}: {len(plans)}")
            for p in plans:
                print(f"  - {p.name} (ID: {p.id})")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())

