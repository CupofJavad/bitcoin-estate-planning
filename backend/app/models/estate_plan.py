"""Estate Plan model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class EstatePlan(Base):
    """Estate Plan model (v1)."""

    __tablename__ = "estate_plans"
    __mapper_args__ = {
        "polymorphic_identity": "estate_plan_v1",
    }

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    bitcoin_address = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships - use string references (will be resolved correctly now)
    beneficiaries = relationship(
        "Beneficiary",
        back_populates="estate_plan",
        cascade="all, delete-orphan"
    )
    timelock_policies = relationship(
        "TimelockPolicy",
        back_populates="estate_plan",
        cascade="all, delete-orphan"
    )

