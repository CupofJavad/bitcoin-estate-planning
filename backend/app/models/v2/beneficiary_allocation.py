"""BeneficiaryAllocation model - Enhanced beneficiary allocation with conditions."""

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class AllocationType(str, enum.Enum):
    """Allocation type enumeration."""
    PERCENTAGE = "PERCENTAGE"
    FIXED_AMOUNT = "FIXED_AMOUNT"
    TIERED = "TIERED"
    CONDITIONAL = "CONDITIONAL"


class InheritanceStyle(str, enum.Enum):
    """Inheritance style enumeration."""
    LUMP_SUM = "LUMP_SUM"
    ANNUITY = "ANNUITY"
    TRANCHE = "TRANCHE"
    TRUST_LIKE_STREAM = "TRUST_LIKE_STREAM"


class BeneficiaryAllocation(Base):
    """BeneficiaryAllocation model - enhanced beneficiary allocation."""

    __tablename__ = "beneficiary_allocations"

    beneficiary_allocation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estate_plan_id = Column(UUID(as_uuid=True), ForeignKey("estate_plans_v2.estate_plan_id", ondelete="CASCADE"), nullable=False)
    beneficiary_party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    allocation_type = Column(SQLEnum(AllocationType), nullable=False)
    allocation_value = Column(Numeric(20, 8), nullable=False)  # Interpretation depends on type
    priority_order = Column(Numeric(5, 2), nullable=True)  # For tiered rules
    conditions_ref = Column(JSONB, nullable=True)  # e.g., "age ≥ 25", "completed education"
    inheritance_style = Column(SQLEnum(InheritanceStyle), default=InheritanceStyle.LUMP_SUM, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    estate_plan = relationship("EstatePlanV2", back_populates="beneficiary_allocations")
    beneficiary_party = relationship("Party", foreign_keys=[beneficiary_party_id])

