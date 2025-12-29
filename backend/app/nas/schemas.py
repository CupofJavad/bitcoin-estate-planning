"""Pydantic schemas for Notification & Audit Service."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.v2.audit_log import ActorType, Criticality
from app.models.v2.notification import DeliveryChannel, DeliveryStatus


# Audit Log Schemas
class AuditLogBase(BaseModel):
    """Base audit log schema."""
    timestamp: datetime
    actor_type: ActorType
    actor_party_id: Optional[UUID] = None
    actor_account_id: Optional[UUID] = None
    event_type: str = Field(..., max_length=100)
    entity_type: Optional[str] = Field(None, max_length=100)
    entity_id: Optional[UUID] = None
    ip_address: Optional[str] = None
    device_id: Optional[UUID] = None
    details: Optional[Dict[str, Any]] = None
    criticality: Criticality = Criticality.INFO


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log."""
    pass


class AuditLogResponse(AuditLogBase):
    """Schema for audit log response."""
    audit_log_id: UUID

    class Config:
        from_attributes = True


# Notification Preference Schemas
class NotificationPreferenceBase(BaseModel):
    """Base notification preference schema."""
    channel: DeliveryChannel
    event_type: str = Field(..., max_length=100)
    enabled: str = "true"  # Boolean as string


class NotificationPreferenceCreate(NotificationPreferenceBase):
    """Schema for creating a notification preference."""
    party_id: UUID


class NotificationPreferenceResponse(NotificationPreferenceBase):
    """Schema for notification preference response."""
    notification_preference_id: UUID
    party_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Notification Schemas
class NotificationBase(BaseModel):
    """Base notification schema."""
    event_type: str = Field(..., max_length=100)
    payload: Optional[Dict[str, Any]] = None
    delivery_channel: DeliveryChannel
    delivery_status: DeliveryStatus = DeliveryStatus.PENDING


class NotificationCreate(NotificationBase):
    """Schema for creating a notification."""
    recipient_party_id: UUID


class NotificationResponse(NotificationBase):
    """Schema for notification response."""
    notification_id: UUID
    recipient_party_id: UUID
    created_at: datetime
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True

