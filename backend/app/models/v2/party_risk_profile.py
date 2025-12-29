"""PartyRiskProfile model - Risk assessment."""

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class OverallRiskLevel(str, enum.Enum):
    """Overall risk level enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class AssessedBy(str, enum.Enum):
    """Assessment source enumeration."""
    AI = "AI"
    HUMAN = "HUMAN"
    MIXED = "MIXED"


class PartyRiskProfile(Base):
    """PartyRiskProfile model - risk assessment for parties."""

    __tablename__ = "party_risk_profiles"

    party_risk_profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False, unique=True)
    overall_risk_level = Column(SQLEnum(OverallRiskLevel), nullable=False)
    risk_factors = Column(JSONB, nullable=True)  # e.g., PEP, cross-border, crypto-heavy
    last_assessed_at = Column(DateTime(timezone=True), nullable=False)
    assessed_by = Column(SQLEnum(AssessedBy), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    party = relationship("Party", foreign_keys=[party_id])

