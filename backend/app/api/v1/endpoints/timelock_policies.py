"""Timelock Policies API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.timelock_policy import TimelockPolicy
from app.schemas.timelock_policy import (
    TimelockPolicyCreate,
    TimelockPolicyUpdate,
    TimelockPolicyResponse,
)

router = APIRouter()


@router.post("/", response_model=TimelockPolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_timelock_policy(
    timelock_policy: TimelockPolicyCreate, db: AsyncSession = Depends(get_db)
) -> TimelockPolicyResponse:
    """Create a new timelock policy."""
    db_timelock_policy = TimelockPolicy(**timelock_policy.model_dump())
    db.add(db_timelock_policy)
    await db.commit()
    await db.refresh(db_timelock_policy)
    return TimelockPolicyResponse.model_validate(db_timelock_policy)


@router.get("/", response_model=List[TimelockPolicyResponse])
async def list_timelock_policies(
    estate_plan_id: int | None = None, db: AsyncSession = Depends(get_db)
) -> List[TimelockPolicyResponse]:
    """List all timelock policies, optionally filtered by estate_plan_id."""
    query = select(TimelockPolicy)
    if estate_plan_id:
        query = query.where(TimelockPolicy.estate_plan_id == estate_plan_id)
    result = await db.execute(query)
    timelock_policies = result.scalars().all()
    return [TimelockPolicyResponse.model_validate(tp) for tp in timelock_policies]


@router.get("/{timelock_policy_id}", response_model=TimelockPolicyResponse)
async def get_timelock_policy(
    timelock_policy_id: int, db: AsyncSession = Depends(get_db)
) -> TimelockPolicyResponse:
    """Get a specific timelock policy."""
    result = await db.execute(
        select(TimelockPolicy).where(TimelockPolicy.id == timelock_policy_id)
    )
    timelock_policy = result.scalar_one_or_none()
    if not timelock_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timelock policy not found"
        )
    return TimelockPolicyResponse.model_validate(timelock_policy)


@router.patch("/{timelock_policy_id}", response_model=TimelockPolicyResponse)
async def update_timelock_policy(
    timelock_policy_id: int,
    timelock_policy_update: TimelockPolicyUpdate,
    db: AsyncSession = Depends(get_db),
) -> TimelockPolicyResponse:
    """Update a timelock policy."""
    result = await db.execute(
        select(TimelockPolicy).where(TimelockPolicy.id == timelock_policy_id)
    )
    timelock_policy = result.scalar_one_or_none()
    if not timelock_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timelock policy not found"
        )

    update_data = timelock_policy_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(timelock_policy, field, value)

    await db.commit()
    await db.refresh(timelock_policy)
    return TimelockPolicyResponse.model_validate(timelock_policy)


@router.delete("/{timelock_policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timelock_policy(
    timelock_policy_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    """Delete a timelock policy."""
    result = await db.execute(
        select(TimelockPolicy).where(TimelockPolicy.id == timelock_policy_id)
    )
    timelock_policy = result.scalar_one_or_none()
    if not timelock_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timelock policy not found"
        )
    await db.delete(timelock_policy)
    await db.commit()

