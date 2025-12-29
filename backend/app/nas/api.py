"""API endpoints for Notification & Audit Service."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.nas.schemas import (
    AuditLogCreate, AuditLogResponse,
    NotificationPreferenceCreate, NotificationPreferenceResponse,
    NotificationCreate, NotificationResponse,
)
from app.nas.service import (
    AuditLogService, NotificationPreferenceService, NotificationService,
)

router = APIRouter(prefix="/v2/nas", tags=["Notification & Audit Service"])


# Audit Log endpoints
@router.post("/audit-logs", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
async def create_audit_log(
    log: AuditLogCreate,
    db: AsyncSession = Depends(get_db),
) -> AuditLogResponse:
    """Create a new audit log entry."""
    return await AuditLogService.create_audit_log(db, log)


@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[UUID] = Query(None),
    actor_party_id: Optional[UUID] = Query(None),
    event_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> List[AuditLogResponse]:
    """Get audit logs with filters."""
    return await AuditLogService.get_audit_logs(
        db,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_party_id=actor_party_id,
        event_type=event_type,
        skip=skip,
        limit=limit,
    )


# Notification Preference endpoints
@router.post("/parties/{party_id}/notification-preferences", response_model=NotificationPreferenceResponse, status_code=status.HTTP_201_CREATED)
async def create_notification_preference(
    party_id: UUID,
    preference: NotificationPreferenceCreate,
    db: AsyncSession = Depends(get_db),
) -> NotificationPreferenceResponse:
    """Create a new notification preference."""
    preference_data = preference.model_dump()
    preference_data["party_id"] = party_id
    return await NotificationPreferenceService.create_preference(db, NotificationPreferenceCreate(**preference_data))


@router.get("/parties/{party_id}/notification-preferences", response_model=List[NotificationPreferenceResponse])
async def get_notification_preferences(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[NotificationPreferenceResponse]:
    """Get all notification preferences for a party."""
    return await NotificationPreferenceService.get_preferences_for_party(db, party_id)


# Notification endpoints
@router.post("/notifications", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification: NotificationCreate,
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """Create a new notification."""
    return await NotificationService.create_notification(db, notification)


@router.get("/parties/{party_id}/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    party_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> List[NotificationResponse]:
    """Get all notifications for a party."""
    return await NotificationService.get_notifications_for_party(db, party_id, skip=skip, limit=limit)


@router.patch("/notifications/{notification_id}/mark-sent", response_model=NotificationResponse)
async def mark_notification_sent(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """Mark a notification as sent."""
    notification = await NotificationService.mark_notification_sent(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return notification

