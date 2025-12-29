"""ContactInfo model - Multiple contact methods per party."""

from sqlalchemy import Column, String, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class ContactType(str, enum.Enum):
    """Contact type enumeration."""
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    ADDRESS = "ADDRESS"
    SOCIAL = "SOCIAL"
    OTHER = "OTHER"


class ContactInfo(Base):
    """ContactInfo model - contact information for parties."""

    __tablename__ = "contact_info"

    contact_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    contact_type = Column(SQLEnum(ContactType), nullable=False)
    value = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    party = relationship("Party", back_populates="contact_info")

