"""EstatePlanParticipant model - Multi-party participation."""

from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class ParticipantRole(str, enum.Enum):
    """Participant role enumeration."""
    CLIENT = "CLIENT"
    PRIMARY_BENEFICIARY = "PRIMARY_BENEFICIARY"
    CONTINGENT_BENEFICIARY = "CONTINGENT_BENEFICIARY"
    EXECUTOR = "EXECUTOR"
    CO_EXECUTOR = "CO_EXECUTOR"
    ATTORNEY_OF_RECORD = "ATTORNEY_OF_RECORD"
    ADVISOR = "ADVISOR"


class EstatePlanParticipant(Base):
    """EstatePlanParticipant model - links parties to estate plans."""

    __tablename__ = "estate_plan_participants"

    estate_plan_participant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estate_plan_id = Column(UUID(as_uuid=True), ForeignKey("estate_plans_v2.estate_plan_id", ondelete="CASCADE"), nullable=False)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(ParticipantRole), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    estate_plan = relationship("EstatePlanV2", back_populates="participants")
    party = relationship("Party", foreign_keys=[party_id])

