"""Business logic for Enhanced Estate Planning Service."""

from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.v2.estate_plan import EstatePlanV2
from app.models.v2.estate_plan_version import EstatePlanVersion
from app.models.v2.estate_plan_participant import EstatePlanParticipant
from app.models.v2.beneficiary_allocation import BeneficiaryAllocation
from app.models.v2.legal_document import LegalDocument
from app.models.v2.life_event import LifeEvent
from app.models.v2.jurisdiction import Jurisdiction
from app.eps.schemas import (
    EstatePlanCreate, EstatePlanUpdate, EstatePlanResponse, EstatePlanWithRelations,
    EstatePlanVersionCreate, EstatePlanVersionResponse,
    EstatePlanParticipantCreate, EstatePlanParticipantResponse,
    BeneficiaryAllocationCreate, BeneficiaryAllocationUpdate, BeneficiaryAllocationResponse,
    LegalDocumentCreate, LegalDocumentUpdate, LegalDocumentResponse,
    LifeEventCreate, LifeEventResponse,
    JurisdictionCreate, JurisdictionResponse,
)


class JurisdictionService:
    """Service for jurisdiction management."""

    @staticmethod
    async def create_jurisdiction(db: AsyncSession, jurisdiction_data: JurisdictionCreate) -> JurisdictionResponse:
        """Create a new jurisdiction."""
        jurisdiction = Jurisdiction(**jurisdiction_data.model_dump())
        db.add(jurisdiction)
        await db.commit()
        await db.refresh(jurisdiction)
        return JurisdictionResponse.model_validate(jurisdiction)

    @staticmethod
    async def get_jurisdiction(db: AsyncSession, jurisdiction_id: UUID) -> Optional[JurisdictionResponse]:
        """Get a jurisdiction by ID."""
        result = await db.execute(select(Jurisdiction).where(Jurisdiction.jurisdiction_id == jurisdiction_id))
        jurisdiction = result.scalar_one_or_none()
        if not jurisdiction:
            return None
        return JurisdictionResponse.model_validate(jurisdiction)

    @staticmethod
    async def list_jurisdictions(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[JurisdictionResponse]:
        """List jurisdictions."""
        result = await db.execute(select(Jurisdiction).offset(skip).limit(limit))
        jurisdictions = result.scalars().all()
        return [JurisdictionResponse.model_validate(j) for j in jurisdictions]


class EstatePlanService:
    """Service for estate plan management."""

    @staticmethod
    async def create_estate_plan(db: AsyncSession, plan_data: EstatePlanCreate) -> EstatePlanResponse:
        """Create a new estate plan."""
        plan = EstatePlanV2(**plan_data.model_dump())
        db.add(plan)
        await db.commit()
        await db.refresh(plan)
        return EstatePlanResponse.model_validate(plan)

    @staticmethod
    async def get_estate_plan(db: AsyncSession, plan_id: UUID) -> Optional[EstatePlanResponse]:
        """Get an estate plan by ID."""
        result = await db.execute(select(EstatePlanV2).where(EstatePlanV2.estate_plan_id == plan_id))
        plan = result.scalar_one_or_none()
        if not plan:
            return None
        return EstatePlanResponse.model_validate(plan)

    @staticmethod
    async def get_estate_plan_with_relations(db: AsyncSession, plan_id: UUID) -> Optional[EstatePlanWithRelations]:
        """Get an estate plan with all relations."""
        result = await db.execute(
            select(EstatePlanV2)
            .where(EstatePlanV2.estate_plan_id == plan_id)
            .options(
                selectinload(EstatePlanV2.versions),
                selectinload(EstatePlanV2.participants),
                selectinload(EstatePlanV2.beneficiary_allocations),
                selectinload(EstatePlanV2.legal_documents),
                selectinload(EstatePlanV2.life_events),
            )
        )
        plan = result.scalar_one_or_none()
        if not plan:
            return None
        return EstatePlanWithRelations.model_validate(plan)

    @staticmethod
    async def list_estate_plans(db: AsyncSession, client_party_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[EstatePlanResponse]:
        """List estate plans."""
        query = select(EstatePlanV2)
        if client_party_id:
            query = query.where(EstatePlanV2.client_party_id == client_party_id)
        result = await db.execute(query.offset(skip).limit(limit))
        plans = result.scalars().all()
        return [EstatePlanResponse.model_validate(p) for p in plans]

    @staticmethod
    async def update_estate_plan(db: AsyncSession, plan_id: UUID, plan_data: EstatePlanUpdate) -> Optional[EstatePlanResponse]:
        """Update an estate plan."""
        update_data = plan_data.model_dump(exclude_unset=True)
        if not update_data:
            return await EstatePlanService.get_estate_plan(db, plan_id)

        await db.execute(
            update(EstatePlanV2)
            .where(EstatePlanV2.estate_plan_id == plan_id)
            .values(**update_data)
        )
        await db.commit()
        return await EstatePlanService.get_estate_plan(db, plan_id)

    @staticmethod
    async def delete_estate_plan(db: AsyncSession, plan_id: UUID) -> bool:
        """Delete an estate plan."""
        result = await db.execute(delete(EstatePlanV2).where(EstatePlanV2.estate_plan_id == plan_id))
        await db.commit()
        return result.rowcount > 0


class EstatePlanVersionService:
    """Service for estate plan version management."""

    @staticmethod
    async def create_version(db: AsyncSession, version_data: EstatePlanVersionCreate) -> EstatePlanVersionResponse:
        """Create a new estate plan version."""
        version = EstatePlanVersion(**version_data.model_dump())
        db.add(version)
        await db.commit()
        await db.refresh(version)
        return EstatePlanVersionResponse.model_validate(version)

    @staticmethod
    async def get_versions_for_plan(db: AsyncSession, plan_id: UUID) -> List[EstatePlanVersionResponse]:
        """Get all versions for an estate plan."""
        result = await db.execute(
            select(EstatePlanVersion)
            .where(EstatePlanVersion.estate_plan_id == plan_id)
            .order_by(EstatePlanVersion.version_number.desc())
        )
        versions = result.scalars().all()
        return [EstatePlanVersionResponse.model_validate(v) for v in versions]


class EstatePlanParticipantService:
    """Service for estate plan participant management."""

    @staticmethod
    async def create_participant(db: AsyncSession, participant_data: EstatePlanParticipantCreate) -> EstatePlanParticipantResponse:
        """Create a new participant."""
        participant = EstatePlanParticipant(**participant_data.model_dump())
        db.add(participant)
        await db.commit()
        await db.refresh(participant)
        return EstatePlanParticipantResponse.model_validate(participant)

    @staticmethod
    async def get_participants_for_plan(db: AsyncSession, plan_id: UUID) -> List[EstatePlanParticipantResponse]:
        """Get all participants for an estate plan."""
        result = await db.execute(
            select(EstatePlanParticipant).where(EstatePlanParticipant.estate_plan_id == plan_id)
        )
        participants = result.scalars().all()
        return [EstatePlanParticipantResponse.model_validate(p) for p in participants]

    @staticmethod
    async def delete_participant(db: AsyncSession, participant_id: UUID) -> bool:
        """Delete a participant."""
        result = await db.execute(delete(EstatePlanParticipant).where(EstatePlanParticipant.estate_plan_participant_id == participant_id))
        await db.commit()
        return result.rowcount > 0


class BeneficiaryAllocationService:
    """Service for beneficiary allocation management."""

    @staticmethod
    async def create_allocation(db: AsyncSession, allocation_data: BeneficiaryAllocationCreate) -> BeneficiaryAllocationResponse:
        """Create a new beneficiary allocation."""
        allocation = BeneficiaryAllocation(**allocation_data.model_dump())
        db.add(allocation)
        await db.commit()
        await db.refresh(allocation)
        return BeneficiaryAllocationResponse.model_validate(allocation)

    @staticmethod
    async def get_allocations_for_plan(db: AsyncSession, plan_id: UUID) -> List[BeneficiaryAllocationResponse]:
        """Get all allocations for an estate plan."""
        result = await db.execute(
            select(BeneficiaryAllocation).where(BeneficiaryAllocation.estate_plan_id == plan_id)
        )
        allocations = result.scalars().all()
        return [BeneficiaryAllocationResponse.model_validate(a) for a in allocations]

    @staticmethod
    async def update_allocation(db: AsyncSession, allocation_id: UUID, allocation_data: BeneficiaryAllocationUpdate) -> Optional[BeneficiaryAllocationResponse]:
        """Update a beneficiary allocation."""
        update_data = allocation_data.model_dump(exclude_unset=True)
        if not update_data:
            result = await db.execute(select(BeneficiaryAllocation).where(BeneficiaryAllocation.beneficiary_allocation_id == allocation_id))
            allocation = result.scalar_one_or_none()
            if allocation:
                return BeneficiaryAllocationResponse.model_validate(allocation)
            return None

        await db.execute(
            update(BeneficiaryAllocation)
            .where(BeneficiaryAllocation.beneficiary_allocation_id == allocation_id)
            .values(**update_data)
        )
        await db.commit()
        result = await db.execute(select(BeneficiaryAllocation).where(BeneficiaryAllocation.beneficiary_allocation_id == allocation_id))
        allocation = result.scalar_one_or_none()
        if allocation:
            return BeneficiaryAllocationResponse.model_validate(allocation)
        return None

    @staticmethod
    async def delete_allocation(db: AsyncSession, allocation_id: UUID) -> bool:
        """Delete a beneficiary allocation."""
        result = await db.execute(delete(BeneficiaryAllocation).where(BeneficiaryAllocation.beneficiary_allocation_id == allocation_id))
        await db.commit()
        return result.rowcount > 0


class LegalDocumentService:
    """Service for legal document management."""

    @staticmethod
    async def create_document(db: AsyncSession, document_data: LegalDocumentCreate) -> LegalDocumentResponse:
        """Create a new legal document."""
        document = LegalDocument(**document_data.model_dump())
        db.add(document)
        await db.commit()
        await db.refresh(document)
        return LegalDocumentResponse.model_validate(document)

    @staticmethod
    async def get_documents_for_plan(db: AsyncSession, plan_id: UUID) -> List[LegalDocumentResponse]:
        """Get all documents for an estate plan."""
        result = await db.execute(
            select(LegalDocument).where(LegalDocument.estate_plan_id == plan_id)
        )
        documents = result.scalars().all()
        return [LegalDocumentResponse.model_validate(d) for d in documents]

    @staticmethod
    async def update_document(db: AsyncSession, document_id: UUID, document_data: LegalDocumentUpdate) -> Optional[LegalDocumentResponse]:
        """Update a legal document."""
        update_data = document_data.model_dump(exclude_unset=True)
        if not update_data:
            result = await db.execute(select(LegalDocument).where(LegalDocument.legal_document_id == document_id))
            document = result.scalar_one_or_none()
            if document:
                return LegalDocumentResponse.model_validate(document)
            return None

        await db.execute(
            update(LegalDocument)
            .where(LegalDocument.legal_document_id == document_id)
            .values(**update_data)
        )
        await db.commit()
        result = await db.execute(select(LegalDocument).where(LegalDocument.legal_document_id == document_id))
        document = result.scalar_one_or_none()
        if document:
            return LegalDocumentResponse.model_validate(document)
        return None

    @staticmethod
    async def delete_document(db: AsyncSession, document_id: UUID) -> bool:
        """Delete a legal document."""
        result = await db.execute(delete(LegalDocument).where(LegalDocument.legal_document_id == document_id))
        await db.commit()
        return result.rowcount > 0


class LifeEventService:
    """Service for life event management."""

    @staticmethod
    async def create_life_event(db: AsyncSession, event_data: LifeEventCreate) -> LifeEventResponse:
        """Create a new life event."""
        event = LifeEvent(**event_data.model_dump())
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return LifeEventResponse.model_validate(event)

    @staticmethod
    async def get_events_for_plan(db: AsyncSession, plan_id: UUID) -> List[LifeEventResponse]:
        """Get all life events for an estate plan."""
        result = await db.execute(
            select(LifeEvent)
            .where(LifeEvent.estate_plan_id == plan_id)
            .order_by(LifeEvent.event_date.desc())
        )
        events = result.scalars().all()
        return [LifeEventResponse.model_validate(e) for e in events]

