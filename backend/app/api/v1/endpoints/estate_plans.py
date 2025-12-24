"""Estate Plans API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.estate_plan import EstatePlan
from app.schemas.estate_plan import (
    EstatePlanCreate,
    EstatePlanUpdate,
    EstatePlanResponse,
    EstatePlanWithRelations,
)

router = APIRouter()


@router.post("/", response_model=EstatePlanResponse, status_code=status.HTTP_201_CREATED)
async def create_estate_plan(
    estate_plan: EstatePlanCreate, db: AsyncSession = Depends(get_db)
) -> EstatePlanResponse:
    """Create a new estate plan."""
    db_estate_plan = EstatePlan(**estate_plan.model_dump())
    db.add(db_estate_plan)
    await db.commit()
    await db.refresh(db_estate_plan)
    return EstatePlanResponse.model_validate(db_estate_plan)


@router.get("/", response_model=List[EstatePlanResponse])
async def list_estate_plans(
    user_id: int | None = None, db: AsyncSession = Depends(get_db)
) -> List[EstatePlanResponse]:
    """List all estate plans, optionally filtered by user_id."""
    query = select(EstatePlan)
    if user_id:
        query = query.where(EstatePlan.user_id == user_id)
    result = await db.execute(query)
    estate_plans = result.scalars().all()
    return [EstatePlanResponse.model_validate(ep) for ep in estate_plans]


@router.get("/{estate_plan_id}", response_model=EstatePlanWithRelations)
async def get_estate_plan(
    estate_plan_id: int, db: AsyncSession = Depends(get_db)
) -> EstatePlanWithRelations:
    """Get a specific estate plan with relations."""
    result = await db.execute(
        select(EstatePlan)
        .where(EstatePlan.id == estate_plan_id)
        .options(
            selectinload(EstatePlan.beneficiaries),
            selectinload(EstatePlan.timelock_policies),
        )
    )
    estate_plan = result.scalar_one_or_none()
    if not estate_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Estate plan not found"
        )
    return EstatePlanWithRelations.model_validate(estate_plan)


@router.patch("/{estate_plan_id}", response_model=EstatePlanResponse)
async def update_estate_plan(
    estate_plan_id: int,
    estate_plan_update: EstatePlanUpdate,
    db: AsyncSession = Depends(get_db),
) -> EstatePlanResponse:
    """Update an estate plan."""
    result = await db.execute(
        select(EstatePlan).where(EstatePlan.id == estate_plan_id)
    )
    estate_plan = result.scalar_one_or_none()
    if not estate_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Estate plan not found"
        )

    update_data = estate_plan_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(estate_plan, field, value)

    await db.commit()
    await db.refresh(estate_plan)
    return EstatePlanResponse.model_validate(estate_plan)


@router.delete("/{estate_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estate_plan(
    estate_plan_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    """Delete an estate plan."""
    result = await db.execute(
        select(EstatePlan).where(EstatePlan.id == estate_plan_id)
    )
    estate_plan = result.scalar_one_or_none()
    if not estate_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Estate plan not found"
        )
    await db.delete(estate_plan)
    await db.commit()

