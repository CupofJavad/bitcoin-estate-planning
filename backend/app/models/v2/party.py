"""Party model - Generic entity for people and organizations."""

from datetime import date
from sqlalchemy import Column, String, Date, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class PartyType(str, enum.Enum):
    """Party type enumeration."""
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"


class PartyStatus(str, enum.Enum):
    """Party status enumeration."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DECEASED = "DECEASED"
    DISSOLVED = "DISSOLVED"


class Party(Base):
    """Party model - represents people and organizations."""

    __tablename__ = "parties"

    party_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    party_type = Column(SQLEnum(PartyType), nullable=False)
    legal_name = Column(String(500), nullable=False)
    preferred_name = Column(String(500), nullable=True)
    date_of_birth = Column(Date, nullable=True)  # For persons
    date_of_incorporation = Column(Date, nullable=True)  # For organizations
    tax_id = Column(String(100), nullable=True)  # SSN, EIN, etc.
    primary_residence_country = Column(String(2), nullable=True)  # ISO country code
    primary_residence_region = Column(String(100), nullable=True)  # State/province
    primary_residence_city = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(SQLEnum(PartyStatus), default=PartyStatus.ACTIVE, nullable=False)

    # Relationships
    roles = relationship("PartyRole", back_populates="party", cascade="all, delete-orphan")
    contact_info = relationship("ContactInfo", back_populates="party", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="party", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="party", cascade="all, delete-orphan")

