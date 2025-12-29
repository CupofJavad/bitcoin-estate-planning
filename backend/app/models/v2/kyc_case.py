"""KYCCase model - KYC workflow tracking."""

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class KYCCaseStatus(str, enum.Enum):
    """KYC case status enumeration."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class RiskLevel(str, enum.Enum):
    """Risk level enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class KYCCase(Base):
    """KYCCase model - KYC workflow tracking."""

    __tablename__ = "kyc_cases"

    kyc_case_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(KYCCaseStatus), default=KYCCaseStatus.PENDING, nullable=False)
    risk_level = Column(SQLEnum(RiskLevel), nullable=True)
    provider = Column(String(200), nullable=True)  # External KYC service
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    party = relationship("Party", foreign_keys=[party_id])
    documents = relationship("KYCDocument", back_populates="kyc_case", cascade="all, delete-orphan")
    sanctions_screenings = relationship("SanctionsScreening", back_populates="kyc_case", cascade="all, delete-orphan")

