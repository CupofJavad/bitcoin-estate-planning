"""Timelock Policy model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class TimelockPolicy(Base):
    """Timelock Policy model."""

    __tablename__ = "timelock_policies"

    id = Column(Integer, primary_key=True, index=True)
    estate_plan_id = Column(Integer, ForeignKey("estate_plans.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    timelock_blocks = Column(Integer, nullable=False)  # Number of blocks to wait
    trigger_condition = Column(String(100), nullable=True)  # e.g., "death", "inactivity", "manual"
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    estate_plan = relationship("EstatePlan", back_populates="timelock_policies")

