"""Device model - Device tracking for security."""

from sqlalchemy import Column, String, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class DeviceType(str, enum.Enum):
    """Device type enumeration."""
    MOBILE = "MOBILE"
    DESKTOP = "DESKTOP"
    HARDWARE_WALLET = "HARDWARE_WALLET"
    UNKNOWN = "UNKNOWN"


class Device(Base):
    """Device model - device tracking for security."""

    __tablename__ = "devices"

    device_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    device_fingerprint = Column(String(255), nullable=False, index=True)
    device_type = Column(SQLEnum(DeviceType), nullable=False)
    os = Column(String(100), nullable=True)
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    trusted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    party = relationship("Party", back_populates="devices")

