"""Enhanced EstatePlan model for v2."""

from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey, Enum as SQLEnum, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class EstatePlanStatus(str, enum.Enum):
    """Estate plan status enumeration."""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class EstatePlanType(str, enum.Enum):
    """Estate plan type enumeration."""
    BITCOIN_ONLY = "BITCOIN_ONLY"
    MULTI_ASSET = "MULTI_ASSET"
    CHARITABLE = "CHARITABLE"
    BUSINESS_SUCCESSION = "BUSINESS_SUCCESSION"
    CUSTOM = "CUSTOM"


class PrimaryCurrency(str, enum.Enum):
    """Primary currency enumeration."""
    USD = "USD"
    EUR = "EUR"
    BTC = "BTC"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"


class EstatePlanV2(Base):
    """Enhanced EstatePlan model for v2."""

    __tablename__ = "estate_plans_v2"
    __mapper_args__ = {
        "polymorphic_identity": "estate_plan_v2",
    }

    estate_plan_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    primary_executor_party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="SET NULL"), nullable=True)
    plan_status = Column(SQLEnum(EstatePlanStatus), default=EstatePlanStatus.DRAFT, nullable=False)
    plan_type = Column(SQLEnum(EstatePlanType), nullable=False)
    governing_jurisdiction_id = Column(UUID(as_uuid=True), ForeignKey("jurisdictions.jurisdiction_id"), nullable=True)
    primary_currency = Column(SQLEnum(PrimaryCurrency), default=PrimaryCurrency.USD, nullable=False)
    effective_date = Column(Date, nullable=True)
    termination_date = Column(Date, nullable=True)
    review_frequency_months = Column(Integer, default=12, nullable=False)
    next_review_due_at = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    client_party = relationship("Party", foreign_keys=[client_party_id], backref="estate_plans_as_client")
    primary_executor_party = relationship("Party", foreign_keys=[primary_executor_party_id])
    governing_jurisdiction = relationship("Jurisdiction", foreign_keys=[governing_jurisdiction_id], back_populates="estate_plans")
    versions = relationship("EstatePlanVersion", back_populates="estate_plan", cascade="all, delete-orphan")
    participants = relationship("EstatePlanParticipant", back_populates="estate_plan", cascade="all, delete-orphan")
    beneficiary_allocations = relationship("BeneficiaryAllocation", back_populates="estate_plan", cascade="all, delete-orphan")
    legal_documents = relationship("LegalDocument", back_populates="estate_plan", cascade="all, delete-orphan")
    life_events = relationship("LifeEvent", back_populates="estate_plan", cascade="all, delete-orphan")
    wallets = relationship("Wallet", back_populates="estate_plan", cascade="all, delete-orphan")

