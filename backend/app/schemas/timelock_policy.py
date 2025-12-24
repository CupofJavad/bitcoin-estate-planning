"""Timelock Policy schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TimelockPolicyBase(BaseModel):
    """Base timelock policy schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    timelock_blocks: int = Field(..., gt=0)
    trigger_condition: Optional[str] = Field(None, max_length=100)


class TimelockPolicyCreate(TimelockPolicyBase):
    """Schema for creating a timelock policy."""

    estate_plan_id: int


class TimelockPolicyUpdate(BaseModel):
    """Schema for updating a timelock policy."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    timelock_blocks: Optional[int] = Field(None, gt=0)
    trigger_condition: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class TimelockPolicyResponse(TimelockPolicyBase):
    """Schema for timelock policy response."""

    id: int
    estate_plan_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

