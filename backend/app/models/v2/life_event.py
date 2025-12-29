"""LifeEvent model - Tracks key events impacting the plan."""

from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey, Enum as SQLEnum, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class LifeEventType(str, enum.Enum):
    """Life event type enumeration."""
    MARRIAGE = "MARRIAGE"
    DIVORCE = "DIVORCE"
    CHILD_BIRTH = "CHILD_BIRTH"
    ADOPTION = "ADOPTION"
    DEATH = "DEATH"
    INCAPACITY = "INCAPACITY"
    MOVE_JURISDICTION = "MOVE_JURISDICTION"
    BUSINESS_SALE = "BUSINESS_SALE"
    MAJOR_ASSET_CHANGE = "MAJOR_ASSET_CHANGE"
    OTHER = "OTHER"


class LifeEvent(Base):
    """LifeEvent model - tracks key events impacting estate plans."""

    __tablename__ = "life_events"

    life_event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estate_plan_id = Column(UUID(as_uuid=True), ForeignKey("estate_plans_v2.estate_plan_id", ondelete="CASCADE"), nullable=False)
    event_type = Column(SQLEnum(LifeEventType), nullable=False)
    subject_party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="SET NULL"), nullable=True)
    event_date = Column(Date, nullable=False)
    evidence_ref = Column(JSONB, nullable=True)  # Documents, external IDs
    notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    recorded_by_party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="SET NULL"), nullable=True)

    # Relationships
    estate_plan = relationship("EstatePlanV2", back_populates="life_events")
    subject_party = relationship("Party", foreign_keys=[subject_party_id])
    recorded_by_party = relationship("Party", foreign_keys=[recorded_by_party_id])

