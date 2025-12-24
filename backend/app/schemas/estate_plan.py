"""Estate Plan schemas."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.beneficiary import BeneficiaryResponse
from app.schemas.timelock_policy import TimelockPolicyResponse


class EstatePlanBase(BaseModel):
    """Base estate plan schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    bitcoin_address: Optional[str] = None


class EstatePlanCreate(EstatePlanBase):
    """Schema for creating an estate plan."""

    user_id: int


class EstatePlanUpdate(BaseModel):
    """Schema for updating an estate plan."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    bitcoin_address: Optional[str] = None
    is_active: Optional[bool] = None


class EstatePlanResponse(EstatePlanBase):
    """Schema for estate plan response."""

    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EstatePlanWithRelations(EstatePlanResponse):
    """Estate plan with related entities."""

    beneficiaries: List[BeneficiaryResponse] = []
    timelock_policies: List[TimelockPolicyResponse] = []

