"""KYCDocument model - Document storage references."""

from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class KYCDocumentType(str, enum.Enum):
    """KYC document type enumeration."""
    PASSPORT = "PASSPORT"
    ID_CARD = "ID_CARD"
    DRIVER_LICENSE = "DRIVER_LICENSE"
    UTILITY_BILL = "UTILITY_BILL"
    BANK_STATEMENT = "BANK_STATEMENT"
    OTHER = "OTHER"


class KYCDocument(Base):
    """KYCDocument model - KYC document storage references."""

    __tablename__ = "kyc_documents"

    kyc_document_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kyc_case_id = Column(UUID(as_uuid=True), ForeignKey("kyc_cases.kyc_case_id", ondelete="CASCADE"), nullable=False)
    document_type = Column(SQLEnum(KYCDocumentType), nullable=False)
    storage_location = Column(String(1000), nullable=False)  # Encrypted file ref
    hash = Column(String(128), nullable=False)
    issue_country = Column(String(2), nullable=True)  # ISO country code
    issue_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    kyc_case = relationship("KYCCase", back_populates="documents")

