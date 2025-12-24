"""Beneficiary schemas."""

from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr


class BeneficiaryBase(BaseModel):
    """Base beneficiary schema."""

    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    bitcoin_address: Optional[str] = None
    allocation_percentage: Decimal = Field(..., ge=0, le=100)


class BeneficiaryCreate(BeneficiaryBase):
    """Schema for creating a beneficiary."""

    estate_plan_id: int


class BeneficiaryUpdate(BaseModel):
    """Schema for updating a beneficiary."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    bitcoin_address: Optional[str] = None
    allocation_percentage: Optional[Decimal] = Field(None, ge=0, le=100)


class BeneficiaryResponse(BeneficiaryBase):
    """Schema for beneficiary response."""

    id: int
    estate_plan_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

