"""Pydantic schemas for Compliance & Risk Service."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.v2.kyc_case import KYCCaseStatus, RiskLevel
from app.models.v2.kyc_document import KYCDocumentType
from app.models.v2.sanctions_screening import ScreeningResult
from app.models.v2.party_risk_profile import OverallRiskLevel, AssessedBy


# KYC Case Schemas
class KYCCaseBase(BaseModel):
    """Base KYC case schema."""
    status: KYCCaseStatus = KYCCaseStatus.PENDING
    risk_level: Optional[RiskLevel] = None
    provider: Optional[str] = Field(None, max_length=200)


class KYCCaseCreate(KYCCaseBase):
    """Schema for creating a KYC case."""
    party_id: UUID


class KYCCaseUpdate(BaseModel):
    """Schema for updating a KYC case."""
    status: Optional[KYCCaseStatus] = None
    risk_level: Optional[RiskLevel] = None
    provider: Optional[str] = Field(None, max_length=200)


class KYCCaseResponse(KYCCaseBase):
    """Schema for KYC case response."""
    kyc_case_id: UUID
    party_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# KYC Document Schemas
class KYCDocumentBase(BaseModel):
    """Base KYC document schema."""
    document_type: KYCDocumentType
    storage_location: str = Field(..., max_length=1000)
    hash: str = Field(..., max_length=128)
    issue_country: Optional[str] = Field(None, max_length=2)
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None


class KYCDocumentCreate(KYCDocumentBase):
    """Schema for creating a KYC document."""
    kyc_case_id: UUID


class KYCDocumentResponse(KYCDocumentBase):
    """Schema for KYC document response."""
    kyc_document_id: UUID
    kyc_case_id: UUID
    verified_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Sanctions Screening Schemas
class SanctionsScreeningBase(BaseModel):
    """Base sanctions screening schema."""
    screening_date: datetime
    result: ScreeningResult
    details: Optional[Dict[str, Any]] = None


class SanctionsScreeningCreate(SanctionsScreeningBase):
    """Schema for creating a sanctions screening."""
    kyc_case_id: UUID


class SanctionsScreeningResponse(SanctionsScreeningBase):
    """Schema for sanctions screening response."""
    sanctions_screening_id: UUID
    kyc_case_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Party Risk Profile Schemas
class PartyRiskProfileBase(BaseModel):
    """Base party risk profile schema."""
    overall_risk_level: OverallRiskLevel
    risk_factors: Optional[Dict[str, Any]] = None
    last_assessed_at: datetime
    assessed_by: AssessedBy


class PartyRiskProfileCreate(PartyRiskProfileBase):
    """Schema for creating a party risk profile."""
    party_id: UUID


class PartyRiskProfileUpdate(BaseModel):
    """Schema for updating a party risk profile."""
    overall_risk_level: Optional[OverallRiskLevel] = None
    risk_factors: Optional[Dict[str, Any]] = None
    last_assessed_at: Optional[datetime] = None
    assessed_by: Optional[AssessedBy] = None


class PartyRiskProfileResponse(PartyRiskProfileBase):
    """Schema for party risk profile response."""
    party_risk_profile_id: UUID
    party_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# KYC Case with Relations
class KYCCaseWithRelations(KYCCaseResponse):
    """KYC case with all relations."""
    documents: List[KYCDocumentResponse] = []
    sanctions_screenings: List[SanctionsScreeningResponse] = []

    class Config:
        from_attributes = True

