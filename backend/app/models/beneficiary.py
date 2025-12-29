"""Beneficiary model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


def _get_estate_plan_class():
    """Get the v1 EstatePlan class to avoid conflicts with v2."""
    from app.models.estate_plan import EstatePlan as EstatePlanV1
    return EstatePlanV1


class Beneficiary(Base):
    """Beneficiary model."""

    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    estate_plan_id = Column(Integer, ForeignKey("estate_plans.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    bitcoin_address = Column(String(255), nullable=True)
    allocation_percentage = Column(Numeric(5, 2), nullable=False)  # 0.00 to 100.00
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships - use class object directly to avoid v2 conflict
    estate_plan = relationship(
        _get_estate_plan_class,
        foreign_keys=[estate_plan_id],
        back_populates="beneficiaries",
    )

