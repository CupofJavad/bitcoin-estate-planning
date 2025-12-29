"""AuditLog model - Comprehensive audit trail."""

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class ActorType(str, enum.Enum):
    """Actor type enumeration."""
    STAFF = "STAFF"
    CLIENT = "CLIENT"
    BENEFICIARY = "BENEFICIARY"
    SYSTEM = "SYSTEM"
    AI = "AI"


class Criticality(str, enum.Enum):
    """Criticality level enumeration."""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AuditLog(Base):
    """AuditLog model - comprehensive audit trail."""

    __tablename__ = "audit_logs"

    audit_log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    actor_type = Column(SQLEnum(ActorType), nullable=False)
    actor_party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="SET NULL"), nullable=True)
    actor_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id", ondelete="SET NULL"), nullable=True)
    event_type = Column(String(100), nullable=False, index=True)  # PLAN_CREATED, DISTRIBUTION_APPROVED, etc.
    entity_type = Column(String(100), nullable=True)  # EstatePlan, Wallet, TriggerEvent, etc.
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    ip_address = Column(INET, nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.device_id", ondelete="SET NULL"), nullable=True)
    details = Column(JSONB, nullable=True)
    criticality = Column(SQLEnum(Criticality), default=Criticality.INFO, nullable=False)

    # Relationships
    actor_party = relationship("Party", foreign_keys=[actor_party_id])
    actor_account = relationship("Account", foreign_keys=[actor_account_id])
    device = relationship("Device", foreign_keys=[device_id])

