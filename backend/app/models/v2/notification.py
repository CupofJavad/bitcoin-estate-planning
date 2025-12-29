"""Notification models - Notification system."""

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class DeliveryChannel(str, enum.Enum):
    """Delivery channel enumeration."""
    EMAIL = "EMAIL"
    SMS = "SMS"
    APP_PUSH = "APP_PUSH"
    PHONE_CALL = "PHONE_CALL"
    IN_APP = "IN_APP"


class DeliveryStatus(str, enum.Enum):
    """Delivery status enumeration."""
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


class NotificationPreference(Base):
    """NotificationPreference model - user notification preferences."""

    __tablename__ = "notification_preferences"

    notification_preference_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    channel = Column(SQLEnum(DeliveryChannel), nullable=False)
    event_type = Column(String(100), nullable=False)  # HEARTBEAT_MISS, DISTRIBUTION_EXECUTED, etc.
    enabled = Column(String(10), default="true", nullable=False)  # Boolean as string for simplicity
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    party = relationship("Party", foreign_keys=[party_id])


class Notification(Base):
    """Notification model - notification records."""

    __tablename__ = "notifications"

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipient_party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSONB, nullable=True)
    delivery_channel = Column(SQLEnum(DeliveryChannel), nullable=False)
    delivery_status = Column(SQLEnum(DeliveryStatus), default=DeliveryStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    recipient_party = relationship("Party", foreign_keys=[recipient_party_id])

