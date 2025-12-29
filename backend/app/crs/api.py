"""API endpoints for Compliance & Risk Service."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crs.schemas import (
    KYCCaseCreate, KYCCaseUpdate, KYCCaseResponse, KYCCaseWithRelations,
    KYCDocumentCreate, KYCDocumentResponse,
    SanctionsScreeningCreate, SanctionsScreeningResponse,
    PartyRiskProfileCreate, PartyRiskProfileResponse,
)
from app.crs.service import (
    KYCCaseService, KYCDocumentService, SanctionsScreeningService, PartyRiskProfileService,
)

router = APIRouter(prefix="/v2/crs", tags=["Compliance & Risk Service"])


# KYC Case endpoints
@router.post("/kyc-cases", response_model=KYCCaseResponse, status_code=status.HTTP_201_CREATED)
async def create_kyc_case(
    case: KYCCaseCreate,
    db: AsyncSession = Depends(get_db),
) -> KYCCaseResponse:
    """Create a new KYC case."""
    return await KYCCaseService.create_kyc_case(db, case)


@router.get("/kyc-cases/{case_id}", response_model=KYCCaseResponse)
async def get_kyc_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> KYCCaseResponse:
    """Get a KYC case by ID."""
    case = await KYCCaseService.get_kyc_case(db, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KYC case not found"
        )
    return case


@router.get("/kyc-cases/{case_id}/full", response_model=KYCCaseWithRelations)
async def get_kyc_case_with_relations(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> KYCCaseWithRelations:
    """Get a KYC case with all relations."""
    case = await KYCCaseService.get_kyc_case_with_relations(db, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KYC case not found"
        )
    return case


@router.get("/parties/{party_id}/kyc-cases", response_model=List[KYCCaseResponse])
async def get_kyc_cases_for_party(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[KYCCaseResponse]:
    """Get all KYC cases for a party."""
    return await KYCCaseService.get_kyc_cases_for_party(db, party_id)


@router.patch("/kyc-cases/{case_id}", response_model=KYCCaseResponse)
async def update_kyc_case(
    case_id: UUID,
    case_update: KYCCaseUpdate,
    db: AsyncSession = Depends(get_db),
) -> KYCCaseResponse:
    """Update a KYC case."""
    case = await KYCCaseService.update_kyc_case(db, case_id, case_update)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KYC case not found"
        )
    return case


# KYC Document endpoints
@router.post("/kyc-cases/{case_id}/documents", response_model=KYCDocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_kyc_document(
    case_id: UUID,
    document: KYCDocumentCreate,
    db: AsyncSession = Depends(get_db),
) -> KYCDocumentResponse:
    """Create a new KYC document."""
    document_data = document.model_dump()
    document_data["kyc_case_id"] = case_id
    return await KYCDocumentService.create_document(db, KYCDocumentCreate(**document_data))


@router.get("/kyc-cases/{case_id}/documents", response_model=List[KYCDocumentResponse])
async def get_kyc_documents(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[KYCDocumentResponse]:
    """Get all documents for a KYC case."""
    return await KYCDocumentService.get_documents_for_case(db, case_id)


# Sanctions Screening endpoints
@router.post("/kyc-cases/{case_id}/sanctions-screenings", response_model=SanctionsScreeningResponse, status_code=status.HTTP_201_CREATED)
async def create_sanctions_screening(
    case_id: UUID,
    screening: SanctionsScreeningCreate,
    db: AsyncSession = Depends(get_db),
) -> SanctionsScreeningResponse:
    """Create a new sanctions screening."""
    screening_data = screening.model_dump()
    screening_data["kyc_case_id"] = case_id
    return await SanctionsScreeningService.create_screening(db, SanctionsScreeningCreate(**screening_data))


@router.get("/kyc-cases/{case_id}/sanctions-screenings", response_model=List[SanctionsScreeningResponse])
async def get_sanctions_screenings(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[SanctionsScreeningResponse]:
    """Get all screenings for a KYC case."""
    return await SanctionsScreeningService.get_screenings_for_case(db, case_id)


# Party Risk Profile endpoints
@router.post("/parties/{party_id}/risk-profiles", response_model=PartyRiskProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_risk_profile(
    party_id: UUID,
    profile: PartyRiskProfileCreate,
    db: AsyncSession = Depends(get_db),
) -> PartyRiskProfileResponse:
    """Create or update a party risk profile."""
    profile_data = profile.model_dump()
    profile_data["party_id"] = party_id
    return await PartyRiskProfileService.create_or_update_risk_profile(db, PartyRiskProfileCreate(**profile_data))


@router.get("/parties/{party_id}/risk-profiles", response_model=PartyRiskProfileResponse)
async def get_risk_profile(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> PartyRiskProfileResponse:
    """Get risk profile for a party."""
    profile = await PartyRiskProfileService.get_risk_profile_for_party(db, party_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk profile not found"
        )
    return profile

