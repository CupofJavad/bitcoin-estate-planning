"""Beneficiaries API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.beneficiary import Beneficiary
from app.schemas.beneficiary import BeneficiaryCreate, BeneficiaryUpdate, BeneficiaryResponse

router = APIRouter()


@router.post("/", response_model=BeneficiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_beneficiary(
    beneficiary: BeneficiaryCreate, db: AsyncSession = Depends(get_db)
) -> BeneficiaryResponse:
    """Create a new beneficiary."""
    db_beneficiary = Beneficiary(**beneficiary.model_dump())
    db.add(db_beneficiary)
    await db.commit()
    await db.refresh(db_beneficiary)
    return BeneficiaryResponse.model_validate(db_beneficiary)


@router.get("/", response_model=List[BeneficiaryResponse])
async def list_beneficiaries(
    estate_plan_id: int | None = None, db: AsyncSession = Depends(get_db)
) -> List[BeneficiaryResponse]:
    """List all beneficiaries, optionally filtered by estate_plan_id."""
    query = select(Beneficiary)
    if estate_plan_id:
        query = query.where(Beneficiary.estate_plan_id == estate_plan_id)
    result = await db.execute(query)
    beneficiaries = result.scalars().all()
    return [BeneficiaryResponse.model_validate(b) for b in beneficiaries]


@router.get("/{beneficiary_id}", response_model=BeneficiaryResponse)
async def get_beneficiary(
    beneficiary_id: int, db: AsyncSession = Depends(get_db)
) -> BeneficiaryResponse:
    """Get a specific beneficiary."""
    result = await db.execute(
        select(Beneficiary).where(Beneficiary.id == beneficiary_id)
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
    db: AsyncSession = Depends(get_db),
) -> BeneficiaryResponse:
    """Update a beneficiary."""
    result = await db.execute(
        select(Beneficiary).where(Beneficiary.id == beneficiary_id)
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
    beneficiary_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    """Delete a beneficiary."""
    result = await db.execute(
        select(Beneficiary).where(Beneficiary.id == beneficiary_id)
    )
    beneficiary = result.scalar_one_or_none()
    if not beneficiary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found"
        )
    await db.delete(beneficiary)
    await db.commit()

