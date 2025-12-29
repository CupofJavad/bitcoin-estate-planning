"""LegalDocument model - Wills, trusts, letters, etc."""

from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey, Enum as SQLEnum, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class LegalDocumentType(str, enum.Enum):
    """Legal document type enumeration."""
    WILL = "WILL"
    TRUST = "TRUST"
    ESTATE_ADDENDUM = "ESTATE_ADDENDUM"
    LETTER_OF_WISHES = "LETTER_OF_WISHES"
    POWER_OF_ATTORNEY = "POWER_OF_ATTORNEY"
    INSURANCE_POLICY = "INSURANCE_POLICY"
    OTHER = "OTHER"


class LegalDocument(Base):
    """LegalDocument model - legal documents."""

    __tablename__ = "legal_documents"

    legal_document_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estate_plan_id = Column(UUID(as_uuid=True), ForeignKey("estate_plans_v2.estate_plan_id", ondelete="CASCADE"), nullable=True)
    document_type = Column(SQLEnum(LegalDocumentType), nullable=False)
    title = Column(String(500), nullable=False)
    storage_location = Column(String(1000), nullable=False)  # Reference to encrypted doc store
    hash = Column(String(128), nullable=False)  # Integrity checksum
    signed_date = Column(Date, nullable=True)
    effective_from = Column(Date, nullable=True)
    effective_to = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    estate_plan = relationship("EstatePlanV2", back_populates="legal_documents")

