"""Pydantic schemas for Enhanced Estate Planning Service."""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field

from app.models.v2.estate_plan import EstatePlanStatus, EstatePlanType, PrimaryCurrency
from app.models.v2.estate_plan_version import VersionStatus
from app.models.v2.estate_plan_participant import ParticipantRole
from app.models.v2.beneficiary_allocation import AllocationType, InheritanceStyle
from app.models.v2.legal_document import LegalDocumentType
from app.models.v2.life_event import LifeEventType


# Jurisdiction Schemas
class JurisdictionBase(BaseModel):
    """Base jurisdiction schema."""
    country_code: str = Field(..., max_length=2)
    region_code: Optional[str] = Field(None, max_length=10)
    name: str = Field(..., max_length=200)
    estate_tax_rules_ref: Optional[str] = None
    inheritance_law_notes: Optional[str] = None
    crypto_regulation_notes: Optional[str] = None


class JurisdictionCreate(JurisdictionBase):
    """Schema for creating a jurisdiction."""
    pass


class JurisdictionResponse(JurisdictionBase):
    """Schema for jurisdiction response."""
    jurisdiction_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Estate Plan Schemas
class EstatePlanBase(BaseModel):
    """Base estate plan schema."""
    plan_type: EstatePlanType
    governing_jurisdiction_id: Optional[UUID] = None
    primary_currency: PrimaryCurrency = PrimaryCurrency.USD
    effective_date: Optional[date] = None
    termination_date: Optional[date] = None
    review_frequency_months: int = Field(12, ge=1, le=120)
    next_review_due_at: Optional[date] = None
    notes: Optional[str] = None
    plan_status: EstatePlanStatus = EstatePlanStatus.DRAFT


class EstatePlanCreate(EstatePlanBase):
    """Schema for creating an estate plan."""
    client_party_id: UUID
    primary_executor_party_id: Optional[UUID] = None


class EstatePlanUpdate(BaseModel):
    """Schema for updating an estate plan."""
    plan_type: Optional[EstatePlanType] = None
    primary_executor_party_id: Optional[UUID] = None
    plan_status: Optional[EstatePlanStatus] = None
    governing_jurisdiction_id: Optional[UUID] = None
    primary_currency: Optional[PrimaryCurrency] = None
    effective_date: Optional[date] = None
    termination_date: Optional[date] = None
    review_frequency_months: Optional[int] = Field(None, ge=1, le=120)
    next_review_due_at: Optional[date] = None
    notes: Optional[str] = None


class EstatePlanResponse(EstatePlanBase):
    """Schema for estate plan response."""
    estate_plan_id: UUID
    client_party_id: UUID
    primary_executor_party_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Estate Plan Version Schemas
class EstatePlanVersionBase(BaseModel):
    """Base estate plan version schema."""
    version_number: int
    status: VersionStatus
    approved_by_party_id: Optional[UUID] = None
    effective_from: datetime
    effective_to: Optional[datetime] = None
    snapshot_data: Optional[Dict[str, Any]] = None


class EstatePlanVersionCreate(EstatePlanVersionBase):
    """Schema for creating an estate plan version."""
    estate_plan_id: UUID


class EstatePlanVersionResponse(EstatePlanVersionBase):
    """Schema for estate plan version response."""
    estate_plan_version_id: UUID
    estate_plan_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Estate Plan Participant Schemas
class EstatePlanParticipantBase(BaseModel):
    """Base estate plan participant schema."""
    role: ParticipantRole
    effective_from: date
    effective_to: Optional[date] = None
    notes: Optional[str] = None


class EstatePlanParticipantCreate(EstatePlanParticipantBase):
    """Schema for creating an estate plan participant."""
    estate_plan_id: UUID
    party_id: UUID


class EstatePlanParticipantResponse(EstatePlanParticipantBase):
    """Schema for estate plan participant response."""
    estate_plan_participant_id: UUID
    estate_plan_id: UUID
    party_id: UUID

    class Config:
        from_attributes = True


# Beneficiary Allocation Schemas
class BeneficiaryAllocationBase(BaseModel):
    """Base beneficiary allocation schema."""
    allocation_type: AllocationType
    allocation_value: Decimal = Field(..., decimal_places=8, max_digits=20)
    priority_order: Optional[Decimal] = Field(None, decimal_places=2, max_digits=5)
    conditions_ref: Optional[Dict[str, Any]] = None
    inheritance_style: InheritanceStyle = InheritanceStyle.LUMP_SUM


class BeneficiaryAllocationCreate(BeneficiaryAllocationBase):
    """Schema for creating a beneficiary allocation."""
    estate_plan_id: UUID
    beneficiary_party_id: UUID


class BeneficiaryAllocationUpdate(BaseModel):
    """Schema for updating a beneficiary allocation."""
    allocation_type: Optional[AllocationType] = None
    allocation_value: Optional[Decimal] = Field(None, decimal_places=8, max_digits=20)
    priority_order: Optional[Decimal] = Field(None, decimal_places=2, max_digits=5)
    conditions_ref: Optional[Dict[str, Any]] = None
    inheritance_style: Optional[InheritanceStyle] = None


class BeneficiaryAllocationResponse(BeneficiaryAllocationBase):
    """Schema for beneficiary allocation response."""
    beneficiary_allocation_id: UUID
    estate_plan_id: UUID
    beneficiary_party_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Legal Document Schemas
class LegalDocumentBase(BaseModel):
    """Base legal document schema."""
    document_type: LegalDocumentType
    title: str = Field(..., max_length=500)
    storage_location: str = Field(..., max_length=1000)
    hash: str = Field(..., max_length=128)
    signed_date: Optional[date] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None


class LegalDocumentCreate(LegalDocumentBase):
    """Schema for creating a legal document."""
    estate_plan_id: Optional[UUID] = None


class LegalDocumentUpdate(BaseModel):
    """Schema for updating a legal document."""
    title: Optional[str] = Field(None, max_length=500)
    storage_location: Optional[str] = Field(None, max_length=1000)
    hash: Optional[str] = Field(None, max_length=128)
    signed_date: Optional[date] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None


class LegalDocumentResponse(LegalDocumentBase):
    """Schema for legal document response."""
    legal_document_id: UUID
    estate_plan_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Life Event Schemas
class LifeEventBase(BaseModel):
    """Base life event schema."""
    event_type: LifeEventType
    subject_party_id: Optional[UUID] = None
    event_date: date
    evidence_ref: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class LifeEventCreate(LifeEventBase):
    """Schema for creating a life event."""
    estate_plan_id: UUID
    recorded_by_party_id: Optional[UUID] = None


class LifeEventResponse(LifeEventBase):
    """Schema for life event response."""
    life_event_id: UUID
    estate_plan_id: UUID
    recorded_at: datetime
    recorded_by_party_id: Optional[UUID] = None

    class Config:
        from_attributes = True


# Estate Plan with Relations
class EstatePlanWithRelations(EstatePlanResponse):
    """Estate plan with all relations."""
    versions: List[EstatePlanVersionResponse] = []
    participants: List[EstatePlanParticipantResponse] = []
    beneficiary_allocations: List[BeneficiaryAllocationResponse] = []
    legal_documents: List[LegalDocumentResponse] = []
    life_events: List[LifeEventResponse] = []

    class Config:
        from_attributes = True

