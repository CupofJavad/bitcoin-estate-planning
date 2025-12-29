"""SanctionsScreening model - Sanctions check results."""

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class ScreeningResult(str, enum.Enum):
    """Screening result enumeration."""
    NO_MATCH = "NO_MATCH"
    POTENTIAL_MATCH = "POTENTIAL_MATCH"
    CONFIRMED_MATCH = "CONFIRMED_MATCH"


class SanctionsScreening(Base):
    """SanctionsScreening model - sanctions screening results."""

    __tablename__ = "sanctions_screenings"

    sanctions_screening_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kyc_case_id = Column(UUID(as_uuid=True), ForeignKey("kyc_cases.kyc_case_id", ondelete="CASCADE"), nullable=False)
    screening_date = Column(DateTime(timezone=True), nullable=False)
    result = Column(SQLEnum(ScreeningResult), nullable=False)
    details = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    kyc_case = relationship("KYCCase", back_populates="sanctions_screenings")

