"""WalletPolicyVersion model - Versioned wallet policies."""

from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class PolicyLanguage(str, enum.Enum):
    """Policy language enumeration."""
    MINISCRIPT = "MINISCRIPT"
    POLICY = "POLICY"
    CUSTOM_SCRIPT = "CUSTOM_SCRIPT"
    EVM_CONTRACT = "EVM_CONTRACT"
    OTHER = "OTHER"


class PolicyVersionStatus(str, enum.Enum):
    """Policy version status enumeration."""
    CURRENT = "CURRENT"
    SUPERSEDED = "SUPERSEDED"


class WalletPolicyVersion(Base):
    """WalletPolicyVersion model - versioned wallet policies."""

    __tablename__ = "wallet_policy_versions"

    wallet_policy_version_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.wallet_id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    status = Column(SQLEnum(PolicyVersionStatus), nullable=False)
    policy_language = Column(SQLEnum(PolicyLanguage), nullable=False)
    policy_text = Column(Text, nullable=True)  # Human-readable policy
    script_template_id = Column(UUID(as_uuid=True), ForeignKey("script_templates.script_template_id"), nullable=True)
    effective_from = Column(DateTime(timezone=True), nullable=False)
    effective_to = Column(DateTime(timezone=True), nullable=True)
    upgrade_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    wallet = relationship("Wallet", back_populates="policy_versions")
    script_template = relationship("ScriptTemplate", back_populates="policy_versions")
    timelock_configs = relationship("TimelockConfig", back_populates="wallet_policy_version", cascade="all, delete-orphan")

