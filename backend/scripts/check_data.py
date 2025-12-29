"""Check database data."""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.estate_plan import EstatePlan
from sqlalchemy import select

async def check():
    async with AsyncSessionLocal() as s:
        # Check users
        u_result = await s.execute(select(User).order_by(User.id))
        users = u_result.scalars().all()
        print(f'Users: {len(users)}')
        for u in users[:5]:
            print(f'  - {u.email} (ID: {u.id})')
        
        if users:
            first_user = users[0]
            # Check estate plans
            ep_result = await s.execute(
                select(EstatePlan).where(EstatePlan.user_id == first_user.id)
            )
            plans = ep_result.scalars().all()
            print(f'\nEstate plans for {first_user.email}: {len(plans)}')
            for p in plans[:5]:
                print(f'  - {p.name} (ID: {p.id}, Active: {p.is_active})')

if __name__ == "__main__":
    asyncio.run(check())

