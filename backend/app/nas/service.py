"""Business logic for Notification & Audit Service."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.models.v2.audit_log import AuditLog
from app.models.v2.notification import Notification, NotificationPreference
from app.nas.schemas import (
    AuditLogCreate, AuditLogResponse,
    NotificationPreferenceCreate, NotificationPreferenceResponse,
    NotificationCreate, NotificationResponse,
)


class AuditLogService:
    """Service for audit logging."""

    @staticmethod
    async def create_audit_log(db: AsyncSession, log_data: AuditLogCreate) -> AuditLogResponse:
        """Create a new audit log entry."""
        log = AuditLog(**log_data.model_dump())
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return AuditLogResponse.model_validate(log)

    @staticmethod
    async def get_audit_logs(
        db: AsyncSession,
        entity_type: Optional[str] = None,
        entity_id: Optional[UUID] = None,
        actor_party_id: Optional[UUID] = None,
        event_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AuditLogResponse]:
        """Get audit logs with filters."""
        query = select(AuditLog)
        if entity_type:
            query = query.where(AuditLog.entity_type == entity_type)
        if entity_id:
            query = query.where(AuditLog.entity_id == entity_id)
        if actor_party_id:
            query = query.where(AuditLog.actor_party_id == actor_party_id)
        if event_type:
            query = query.where(AuditLog.event_type == event_type)
        
        result = await db.execute(query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit))
        logs = result.scalars().all()
        return [AuditLogResponse.model_validate(l) for l in logs]


class NotificationPreferenceService:
    """Service for notification preference management."""

    @staticmethod
    async def create_preference(db: AsyncSession, preference_data: NotificationPreferenceCreate) -> NotificationPreferenceResponse:
        """Create a new notification preference."""
        preference = NotificationPreference(**preference_data.model_dump())
        db.add(preference)
        await db.commit()
        await db.refresh(preference)
        return NotificationPreferenceResponse.model_validate(preference)

    @staticmethod
    async def get_preferences_for_party(db: AsyncSession, party_id: UUID) -> List[NotificationPreferenceResponse]:
        """Get all notification preferences for a party."""
        result = await db.execute(select(NotificationPreference).where(NotificationPreference.party_id == party_id))
        preferences = result.scalars().all()
        return [NotificationPreferenceResponse.model_validate(p) for p in preferences]


class NotificationService:
    """Service for notification management."""

    @staticmethod
    async def create_notification(db: AsyncSession, notification_data: NotificationCreate) -> NotificationResponse:
        """Create a new notification."""
        notification = Notification(**notification_data.model_dump())
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return NotificationResponse.model_validate(notification)

    @staticmethod
    async def get_notifications_for_party(
        db: AsyncSession,
        party_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[NotificationResponse]:
        """Get all notifications for a party."""
        result = await db.execute(
            select(Notification)
            .where(Notification.recipient_party_id == party_id)
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        notifications = result.scalars().all()
        return [NotificationResponse.model_validate(n) for n in notifications]

    @staticmethod
    async def mark_notification_sent(db: AsyncSession, notification_id: UUID) -> Optional[NotificationResponse]:
        """Mark a notification as sent."""
        from datetime import datetime
        from app.models.v2.notification import DeliveryStatus
        await db.execute(
            update(Notification)
            .where(Notification.notification_id == notification_id)
            .values(delivery_status=DeliveryStatus.SENT, sent_at=datetime.utcnow())
        )
        await db.commit()
        result = await db.execute(select(Notification).where(Notification.notification_id == notification_id))
        notification = result.scalar_one_or_none()
        if notification:
            return NotificationResponse.model_validate(notification)
        return None

