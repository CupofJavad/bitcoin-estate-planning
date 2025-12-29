"""Business logic for Compliance & Risk Service."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.v2.kyc_case import KYCCase
from app.models.v2.kyc_document import KYCDocument
from app.models.v2.sanctions_screening import SanctionsScreening
from app.models.v2.party_risk_profile import PartyRiskProfile
from app.crs.schemas import (
    KYCCaseCreate, KYCCaseUpdate, KYCCaseResponse, KYCCaseWithRelations,
    KYCDocumentCreate, KYCDocumentResponse,
    SanctionsScreeningCreate, SanctionsScreeningResponse,
    PartyRiskProfileCreate, PartyRiskProfileUpdate, PartyRiskProfileResponse,
)


class KYCCaseService:
    """Service for KYC case management."""

    @staticmethod
    async def create_kyc_case(db: AsyncSession, case_data: KYCCaseCreate) -> KYCCaseResponse:
        """Create a new KYC case."""
        case = KYCCase(**case_data.model_dump())
        db.add(case)
        await db.commit()
        await db.refresh(case)
        return KYCCaseResponse.model_validate(case)

    @staticmethod
    async def get_kyc_case(db: AsyncSession, case_id: UUID) -> Optional[KYCCaseResponse]:
        """Get a KYC case by ID."""
        result = await db.execute(select(KYCCase).where(KYCCase.kyc_case_id == case_id))
        case = result.scalar_one_or_none()
        if not case:
            return None
        return KYCCaseResponse.model_validate(case)

    @staticmethod
    async def get_kyc_case_with_relations(db: AsyncSession, case_id: UUID) -> Optional[KYCCaseWithRelations]:
        """Get a KYC case with all relations."""
        result = await db.execute(
            select(KYCCase)
            .where(KYCCase.kyc_case_id == case_id)
            .options(
                selectinload(KYCCase.documents),
                selectinload(KYCCase.sanctions_screenings),
            )
        )
        case = result.scalar_one_or_none()
        if not case:
            return None
        return KYCCaseWithRelations.model_validate(case)

    @staticmethod
    async def get_kyc_cases_for_party(db: AsyncSession, party_id: UUID) -> List[KYCCaseResponse]:
        """Get all KYC cases for a party."""
        result = await db.execute(select(KYCCase).where(KYCCase.party_id == party_id))
        cases = result.scalars().all()
        return [KYCCaseResponse.model_validate(c) for c in cases]

    @staticmethod
    async def update_kyc_case(db: AsyncSession, case_id: UUID, case_data: KYCCaseUpdate) -> Optional[KYCCaseResponse]:
        """Update a KYC case."""
        update_data = case_data.model_dump(exclude_unset=True)
        if not update_data:
            return await KYCCaseService.get_kyc_case(db, case_id)

        await db.execute(
            update(KYCCase)
            .where(KYCCase.kyc_case_id == case_id)
            .values(**update_data)
        )
        await db.commit()
        return await KYCCaseService.get_kyc_case(db, case_id)


class KYCDocumentService:
    """Service for KYC document management."""

    @staticmethod
    async def create_document(db: AsyncSession, document_data: KYCDocumentCreate) -> KYCDocumentResponse:
        """Create a new KYC document."""
        document = KYCDocument(**document_data.model_dump())
        db.add(document)
        await db.commit()
        await db.refresh(document)
        return KYCDocumentResponse.model_validate(document)

    @staticmethod
    async def get_documents_for_case(db: AsyncSession, case_id: UUID) -> List[KYCDocumentResponse]:
        """Get all documents for a KYC case."""
        result = await db.execute(select(KYCDocument).where(KYCDocument.kyc_case_id == case_id))
        documents = result.scalars().all()
        return [KYCDocumentResponse.model_validate(d) for d in documents]


class SanctionsScreeningService:
    """Service for sanctions screening management."""

    @staticmethod
    async def create_screening(db: AsyncSession, screening_data: SanctionsScreeningCreate) -> SanctionsScreeningResponse:
        """Create a new sanctions screening."""
        screening = SanctionsScreening(**screening_data.model_dump())
        db.add(screening)
        await db.commit()
        await db.refresh(screening)
        return SanctionsScreeningResponse.model_validate(screening)

    @staticmethod
    async def get_screenings_for_case(db: AsyncSession, case_id: UUID) -> List[SanctionsScreeningResponse]:
        """Get all screenings for a KYC case."""
        result = await db.execute(select(SanctionsScreening).where(SanctionsScreening.kyc_case_id == case_id))
        screenings = result.scalars().all()
        return [SanctionsScreeningResponse.model_validate(s) for s in screenings]


class PartyRiskProfileService:
    """Service for party risk profile management."""

    @staticmethod
    async def create_or_update_risk_profile(db: AsyncSession, profile_data: PartyRiskProfileCreate) -> PartyRiskProfileResponse:
        """Create or update a party risk profile."""
        result = await db.execute(
            select(PartyRiskProfile).where(PartyRiskProfile.party_id == profile_data.party_id)
        )
        profile = result.scalar_one_or_none()

        if profile:
            # Update existing profile
            for key, value in profile_data.model_dump(exclude={"party_id"}).items():
                setattr(profile, key, value)
        else:
            # Create new profile
            profile = PartyRiskProfile(**profile_data.model_dump())
            db.add(profile)

        await db.commit()
        await db.refresh(profile)
        return PartyRiskProfileResponse.model_validate(profile)

    @staticmethod
    async def get_risk_profile_for_party(db: AsyncSession, party_id: UUID) -> Optional[PartyRiskProfileResponse]:
        """Get risk profile for a party."""
        result = await db.execute(select(PartyRiskProfile).where(PartyRiskProfile.party_id == party_id))
        profile = result.scalar_one_or_none()
        if not profile:
            return None
        return PartyRiskProfileResponse.model_validate(profile)

