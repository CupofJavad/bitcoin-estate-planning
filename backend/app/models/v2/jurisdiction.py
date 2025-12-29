"""Jurisdiction model - Legal jurisdiction data."""

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Jurisdiction(Base):
    """Jurisdiction model - legal jurisdiction information."""

    __tablename__ = "jurisdictions"

    jurisdiction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_code = Column(String(2), nullable=False, index=True)  # ISO country code
    region_code = Column(String(10), nullable=True, index=True)  # State/province code
    name = Column(String(200), nullable=False)  # "California, USA"
    estate_tax_rules_ref = Column(Text, nullable=True)  # Reference to rule engine config
    inheritance_law_notes = Column(Text, nullable=True)
    crypto_regulation_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships - reference EstatePlanV2 to avoid conflict with v1 model
    estate_plans = relationship("EstatePlanV2", back_populates="governing_jurisdiction")

