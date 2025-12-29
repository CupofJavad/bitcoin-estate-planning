"""ScriptTemplate model - Reusable script/policy templates."""

from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class ScriptTemplate(Base):
    """ScriptTemplate model - reusable script/policy templates."""

    __tablename__ = "script_templates"

    script_template_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    policy_language = Column(String(50), nullable=False)  # MINISCRIPT, POLICY, etc.
    policy_template_text = Column(Text, nullable=False)  # With placeholders
    default_parameters = Column(JSONB, nullable=True)
    supports_pqc = Column(Boolean, default=False, nullable=False)  # Post-quantum cryptography support
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    policy_versions = relationship("WalletPolicyVersion", back_populates="script_template")

