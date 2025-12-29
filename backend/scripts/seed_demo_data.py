"""Seed demo data for Bitcoin Estate Planning Platform.

Creates sample estate plans, beneficiaries, and timelock policies
for demonstration purposes.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal as async_session_maker
from app.models.user import User
from app.models.estate_plan import EstatePlan
from app.models.beneficiary import Beneficiary
from app.models.timelock_policy import TimelockPolicy
from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Direct bcrypt hashing to avoid passlib version issues
def hash_password(password: str) -> str:
    """Hash password using bcrypt directly."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


async def create_demo_user(session: AsyncSession) -> User:
    """Create or get demo user."""
    # Check if demo user exists
    result = await session.execute(
        select(User).where(User.email == "demo@example.com")
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        print(f"Demo user already exists: {existing_user.email} (ID: {existing_user.id})")
        return existing_user
    
    # Create new demo user
    # Use the expected demo password
    password = "demo123456"
    hashed_password = hash_password(password)
    
    demo_user = User(
        email="demo@example.com",
        hashed_password=hashed_password,
        full_name="Demo User",
        is_active=True,
        is_verified=True,
    )
    
    session.add(demo_user)
    await session.commit()
    await session.refresh(demo_user)
    
    return demo_user


async def seed_demo_data():
    """Seed demo data."""
    async with async_session_maker() as session:
        try:
            # Create demo user
            print("Creating demo user...")
            demo_user = await create_demo_user(session)
            print(f"Demo user created: {demo_user.email} (ID: {demo_user.id})")

            # Create estate plans
            estate_plans_data = [
                {
                    "name": "Main Bitcoin Estate",
                    "description": "Primary estate plan for Bitcoin inheritance",
                    "bitcoin_address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                    "is_active": True,
                },
                {
                    "name": "Family Trust Estate",
                    "description": "Estate plan for family trust beneficiaries",
                    "bitcoin_address": "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0slvdk",
                    "is_active": True,
                },
                {
                    "name": "Charitable Giving Plan",
                    "description": "Estate plan for charitable organizations",
                    "bitcoin_address": None,
                    "is_active": False,
                },
            ]

            estate_plans = []
            for plan_data in estate_plans_data:
                estate_plan = EstatePlan(
                    user_id=demo_user.id,
                    **plan_data,
                )
                session.add(estate_plan)
                estate_plans.append(estate_plan)

            await session.commit()
            
            for plan in estate_plans:
                await session.refresh(plan)
            print(f"Created {len(estate_plans)} estate plans")

            # Create beneficiaries
            beneficiaries_data = [
                {
                    "estate_plan_id": estate_plans[0].id,
                    "name": "Alice Johnson",
                    "email": "alice@example.com",
                    "bitcoin_address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                    "allocation_percentage": 50.0,
                },
                {
                    "estate_plan_id": estate_plans[0].id,
                    "name": "Bob Smith",
                    "email": "bob@example.com",
                    "bitcoin_address": None,
                    "allocation_percentage": 30.0,
                },
                {
                    "estate_plan_id": estate_plans[0].id,
                    "name": "Charlie Brown",
                    "email": "charlie@example.com",
                    "bitcoin_address": None,
                    "allocation_percentage": 20.0,
                },
                {
                    "estate_plan_id": estate_plans[1].id,
                    "name": "Diana Prince",
                    "email": "diana@example.com",
                    "bitcoin_address": None,
                    "allocation_percentage": 60.0,
                },
                {
                    "estate_plan_id": estate_plans[1].id,
                    "name": "Edward Norton",
                    "email": "edward@example.com",
                    "bitcoin_address": None,
                    "allocation_percentage": 40.0,
                },
            ]

            for beneficiary_data in beneficiaries_data:
                beneficiary = Beneficiary(**beneficiary_data)
                session.add(beneficiary)

            await session.commit()
            print(f"Created {len(beneficiaries_data)} beneficiaries")

            # Create timelock policies
            policies_data = [
                {
                    "estate_plan_id": estate_plans[0].id,
                    "name": "Death Trigger Policy",
                    "description": "Activates upon death certificate verification",
                    "timelock_blocks": 1440,  # ~10 days
                    "trigger_condition": "death",
                    "is_active": True,
                },
                {
                    "estate_plan_id": estate_plans[0].id,
                    "name": "Inactivity Policy",
                    "description": "Activates after 90 days of inactivity",
                    "timelock_blocks": 12960,  # ~90 days
                    "trigger_condition": "inactivity",
                    "is_active": True,
                },
                {
                    "estate_plan_id": estate_plans[1].id,
                    "name": "Manual Release",
                    "description": "Manual activation by estate executor",
                    "timelock_blocks": 0,
                    "trigger_condition": "manual",
                    "is_active": True,
                },
            ]

            for policy_data in policies_data:
                policy = TimelockPolicy(**policy_data)
                session.add(policy)

            await session.commit()
            print(f"Created {len(policies_data)} timelock policies")

            print("\n✅ Demo data seeded successfully!")
            print(f"\nDemo user credentials:")
            print(f"  Email: demo@example.com")
            print(f"  Password: demo123456")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding data: {str(e)}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_demo_data())

