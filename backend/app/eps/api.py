"""API endpoints for Enhanced Estate Planning Service."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.eps.schemas import (
    JurisdictionCreate, JurisdictionResponse,
    EstatePlanCreate, EstatePlanUpdate, EstatePlanResponse, EstatePlanWithRelations,
    EstatePlanVersionCreate, EstatePlanVersionResponse,
    EstatePlanParticipantCreate, EstatePlanParticipantResponse,
    BeneficiaryAllocationCreate, BeneficiaryAllocationUpdate, BeneficiaryAllocationResponse,
    LegalDocumentCreate, LegalDocumentUpdate, LegalDocumentResponse,
    LifeEventCreate, LifeEventResponse,
)
from app.eps.service import (
    JurisdictionService, EstatePlanService, EstatePlanVersionService,
    EstatePlanParticipantService, BeneficiaryAllocationService,
    LegalDocumentService, LifeEventService,
)

router = APIRouter(prefix="/v2/eps", tags=["Enhanced Estate Planning Service"])


# Jurisdiction endpoints
@router.post("/jurisdictions", response_model=JurisdictionResponse, status_code=status.HTTP_201_CREATED)
async def create_jurisdiction(
    jurisdiction: JurisdictionCreate,
    db: AsyncSession = Depends(get_db),
) -> JurisdictionResponse:
    """Create a new jurisdiction."""
    return await JurisdictionService.create_jurisdiction(db, jurisdiction)


@router.get("/jurisdictions/{jurisdiction_id}", response_model=JurisdictionResponse)
async def get_jurisdiction(
    jurisdiction_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> JurisdictionResponse:
    """Get a jurisdiction by ID."""
    jurisdiction = await JurisdictionService.get_jurisdiction(db, jurisdiction_id)
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jurisdiction not found"
        )
    return jurisdiction


@router.get("/jurisdictions", response_model=List[JurisdictionResponse])
async def list_jurisdictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> List[JurisdictionResponse]:
    """List jurisdictions."""
    return await JurisdictionService.list_jurisdictions(db, skip=skip, limit=limit)


# Estate Plan endpoints
@router.post("/estate-plans", response_model=EstatePlanResponse, status_code=status.HTTP_201_CREATED)
async def create_estate_plan(
    plan: EstatePlanCreate,
    db: AsyncSession = Depends(get_db),
) -> EstatePlanResponse:
    """Create a new estate plan."""
    return await EstatePlanService.create_estate_plan(db, plan)


@router.get("/estate-plans/{plan_id}", response_model=EstatePlanResponse)
async def get_estate_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> EstatePlanResponse:
    """Get an estate plan by ID."""
    plan = await EstatePlanService.get_estate_plan(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate plan not found"
        )
    return plan


@router.get("/estate-plans/{plan_id}/full", response_model=EstatePlanWithRelations)
async def get_estate_plan_with_relations(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> EstatePlanWithRelations:
    """Get an estate plan with all relations."""
    plan = await EstatePlanService.get_estate_plan_with_relations(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate plan not found"
        )
    return plan


@router.get("/estate-plans", response_model=List[EstatePlanResponse])
async def list_estate_plans(
    client_party_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> List[EstatePlanResponse]:
    """List estate plans."""
    return await EstatePlanService.list_estate_plans(db, client_party_id=client_party_id, skip=skip, limit=limit)


@router.patch("/estate-plans/{plan_id}", response_model=EstatePlanResponse)
async def update_estate_plan(
    plan_id: UUID,
    plan_update: EstatePlanUpdate,
    db: AsyncSession = Depends(get_db),
) -> EstatePlanResponse:
    """Update an estate plan."""
    plan = await EstatePlanService.update_estate_plan(db, plan_id, plan_update)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate plan not found"
        )
    return plan


@router.delete("/estate-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estate_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete an estate plan."""
    deleted = await EstatePlanService.delete_estate_plan(db, plan_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estate plan not found"
        )


# Estate Plan Version endpoints
@router.post("/estate-plans/{plan_id}/versions", response_model=EstatePlanVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_estate_plan_version(
    plan_id: UUID,
    version: EstatePlanVersionCreate,
    db: AsyncSession = Depends(get_db),
) -> EstatePlanVersionResponse:
    """Create a new version for an estate plan."""
    version_data = version.model_dump()
    version_data["estate_plan_id"] = plan_id
    return await EstatePlanVersionService.create_version(db, EstatePlanVersionCreate(**version_data))


@router.get("/estate-plans/{plan_id}/versions", response_model=List[EstatePlanVersionResponse])
async def get_estate_plan_versions(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[EstatePlanVersionResponse]:
    """Get all versions for an estate plan."""
    return await EstatePlanVersionService.get_versions_for_plan(db, plan_id)


# Estate Plan Participant endpoints
@router.post("/estate-plans/{plan_id}/participants", response_model=EstatePlanParticipantResponse, status_code=status.HTTP_201_CREATED)
async def create_participant(
    plan_id: UUID,
    participant: EstatePlanParticipantCreate,
    db: AsyncSession = Depends(get_db),
) -> EstatePlanParticipantResponse:
    """Create a new participant for an estate plan."""
    participant_data = participant.model_dump()
    participant_data["estate_plan_id"] = plan_id
    return await EstatePlanParticipantService.create_participant(db, EstatePlanParticipantCreate(**participant_data))


@router.get("/estate-plans/{plan_id}/participants", response_model=List[EstatePlanParticipantResponse])
async def get_participants(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[EstatePlanParticipantResponse]:
    """Get all participants for an estate plan."""
    return await EstatePlanParticipantService.get_participants_for_plan(db, plan_id)


@router.delete("/participants/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_participant(
    participant_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a participant."""
    deleted = await EstatePlanParticipantService.delete_participant(db, participant_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found"
        )


# Beneficiary Allocation endpoints
@router.post("/estate-plans/{plan_id}/beneficiary-allocations", response_model=BeneficiaryAllocationResponse, status_code=status.HTTP_201_CREATED)
async def create_beneficiary_allocation(
    plan_id: UUID,
    allocation: BeneficiaryAllocationCreate,
    db: AsyncSession = Depends(get_db),
) -> BeneficiaryAllocationResponse:
    """Create a new beneficiary allocation."""
    allocation_data = allocation.model_dump()
    allocation_data["estate_plan_id"] = plan_id
    return await BeneficiaryAllocationService.create_allocation(db, BeneficiaryAllocationCreate(**allocation_data))


@router.get("/estate-plans/{plan_id}/beneficiary-allocations", response_model=List[BeneficiaryAllocationResponse])
async def get_beneficiary_allocations(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[BeneficiaryAllocationResponse]:
    """Get all beneficiary allocations for an estate plan."""
    return await BeneficiaryAllocationService.get_allocations_for_plan(db, plan_id)


@router.patch("/beneficiary-allocations/{allocation_id}", response_model=BeneficiaryAllocationResponse)
async def update_beneficiary_allocation(
    allocation_id: UUID,
    allocation_update: BeneficiaryAllocationUpdate,
    db: AsyncSession = Depends(get_db),
) -> BeneficiaryAllocationResponse:
    """Update a beneficiary allocation."""
    allocation = await BeneficiaryAllocationService.update_allocation(db, allocation_id, allocation_update)
    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Beneficiary allocation not found"
        )
    return allocation


@router.delete("/beneficiary-allocations/{allocation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_beneficiary_allocation(
    allocation_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a beneficiary allocation."""
    deleted = await BeneficiaryAllocationService.delete_allocation(db, allocation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Beneficiary allocation not found"
        )


# Legal Document endpoints
@router.post("/estate-plans/{plan_id}/legal-documents", response_model=LegalDocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_legal_document(
    plan_id: UUID,
    document: LegalDocumentCreate,
    db: AsyncSession = Depends(get_db),
) -> LegalDocumentResponse:
    """Create a new legal document."""
    document_data = document.model_dump()
    document_data["estate_plan_id"] = plan_id
    return await LegalDocumentService.create_document(db, LegalDocumentCreate(**document_data))


@router.get("/estate-plans/{plan_id}/legal-documents", response_model=List[LegalDocumentResponse])
async def get_legal_documents(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[LegalDocumentResponse]:
    """Get all legal documents for an estate plan."""
    return await LegalDocumentService.get_documents_for_plan(db, plan_id)


@router.patch("/legal-documents/{document_id}", response_model=LegalDocumentResponse)
async def update_legal_document(
    document_id: UUID,
    document_update: LegalDocumentUpdate,
    db: AsyncSession = Depends(get_db),
) -> LegalDocumentResponse:
    """Update a legal document."""
    document = await LegalDocumentService.update_document(db, document_id, document_update)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legal document not found"
        )
    return document


@router.delete("/legal-documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_legal_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a legal document."""
    deleted = await LegalDocumentService.delete_document(db, document_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legal document not found"
        )


# Life Event endpoints
@router.post("/estate-plans/{plan_id}/life-events", response_model=LifeEventResponse, status_code=status.HTTP_201_CREATED)
async def create_life_event(
    plan_id: UUID,
    event: LifeEventCreate,
    db: AsyncSession = Depends(get_db),
) -> LifeEventResponse:
    """Create a new life event."""
    event_data = event.model_dump()
    event_data["estate_plan_id"] = plan_id
    return await LifeEventService.create_life_event(db, LifeEventCreate(**event_data))


@router.get("/estate-plans/{plan_id}/life-events", response_model=List[LifeEventResponse])
async def get_life_events(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[LifeEventResponse]:
    """Get all life events for an estate plan."""
    return await LifeEventService.get_events_for_plan(db, plan_id)

