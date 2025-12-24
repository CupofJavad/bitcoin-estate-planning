"""Beneficiaries API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.users import current_user
from app.models.beneficiary import Beneficiary
from app.models.estate_plan import EstatePlan
from app.models.user import User
from app.schemas.beneficiary import BeneficiaryCreate, BeneficiaryUpdate, BeneficiaryResponse

router = APIRouter()


@router.post("/", response_model=BeneficiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_beneficiary(
    beneficiary: BeneficiaryCreate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> BeneficiaryResponse:
    """Create a new beneficiary (only for user's estate plans)."""
    # Verify estate plan belongs to user
    estate_plan_result = await db.execute(
        select(EstatePlan)
        .where(EstatePlan.id == beneficiary.estate_plan_id)
        .where(EstatePlan.user_id == user.id)
    )
    estate_plan = estate_plan_result.scalar_one_or_none()
    if not estate_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate plan not found or access denied",
        )
    
    db_beneficiary = Beneficiary(**beneficiary.model_dump())
    db.add(db_beneficiary)
    await db.commit()
    await db.refresh(db_beneficiary)
    return BeneficiaryResponse.model_validate(db_beneficiary)


@router.get("/", response_model=List[BeneficiaryResponse])
async def list_beneficiaries(
    estate_plan_id: int | None = None,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> List[BeneficiaryResponse]:
    """List beneficiaries for user's estate plans."""
    # Join with EstatePlan to filter by user_id
    query = (
        select(Beneficiary)
        .join(EstatePlan)
        .where(EstatePlan.user_id == user.id)
    )
    if estate_plan_id:
        query = query.where(Beneficiary.estate_plan_id == estate_plan_id)
    result = await db.execute(query)
    beneficiaries = result.scalars().all()
    return [BeneficiaryResponse.model_validate(b) for b in beneficiaries]


@router.get("/{beneficiary_id}", response_model=BeneficiaryResponse)
async def get_beneficiary(
    beneficiary_id: int,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> BeneficiaryResponse:
    """Get a specific beneficiary (only if belongs to user's estate plan)."""
    result = await db.execute(
        select(Beneficiary)
        .join(EstatePlan)
        .where(Beneficiary.id == beneficiary_id)
        .where(EstatePlan.user_id == user.id)
    )
    beneficiary = result.scalar_one_or_none()
    if not beneficiary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found"
        )
    return BeneficiaryResponse.model_validate(beneficiary)


@router.patch("/{beneficiary_id}", response_model=BeneficiaryResponse)
async def update_beneficiary(
    beneficiary_id: int,
    beneficiary_update: BeneficiaryUpdate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> BeneficiaryResponse:
    """Update a beneficiary (only if belongs to user's estate plan)."""
    result = await db.execute(
        select(Beneficiary)
        .join(EstatePlan)
        .where(Beneficiary.id == beneficiary_id)
        .where(EstatePlan.user_id == user.id)
    )
    beneficiary = result.scalar_one_or_none()
    if not beneficiary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found"
        )

    update_data = beneficiary_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(beneficiary, field, value)

    await db.commit()
    await db.refresh(beneficiary)
    return BeneficiaryResponse.model_validate(beneficiary)


@router.delete("/{beneficiary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_beneficiary(
    beneficiary_id: int,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a beneficiary (only if belongs to user's estate plan)."""
    result = await db.execute(
        select(Beneficiary)
        .join(EstatePlan)
        .where(Beneficiary.id == beneficiary_id)
        .where(EstatePlan.user_id == user.id)
    )
    beneficiary = result.scalar_one_or_none()
    if not beneficiary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found"
        )
    await db.delete(beneficiary)
    await db.commit()

