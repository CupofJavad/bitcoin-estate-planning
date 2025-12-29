"""EstatePlanVersion model - Versioned snapshots for audit."""

from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class VersionStatus(str, enum.Enum):
    """Version status enumeration."""
    CURRENT = "CURRENT"
    SUPERSEDED = "SUPERSEDED"
    REVOKED = "REVOKED"


class EstatePlanVersion(Base):
    """EstatePlanVersion model - versioned snapshots for audit."""

    __tablename__ = "estate_plan_versions"

    estate_plan_version_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estate_plan_id = Column(UUID(as_uuid=True), ForeignKey("estate_plans_v2.estate_plan_id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    status = Column(SQLEnum(VersionStatus), nullable=False)
    approved_by_party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="SET NULL"), nullable=True)
    effective_from = Column(DateTime(timezone=True), nullable=False)
    effective_to = Column(DateTime(timezone=True), nullable=True)
    snapshot_data = Column(JSONB, nullable=True)  # Denormalized capture of relevant structure
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    estate_plan = relationship("EstatePlanV2", back_populates="versions")
    approved_by_party = relationship("Party", foreign_keys=[approved_by_party_id])

