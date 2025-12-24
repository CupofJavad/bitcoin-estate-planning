"""Beneficiary model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


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

    # Relationships
    estate_plan = relationship("EstatePlan", back_populates="beneficiaries")

