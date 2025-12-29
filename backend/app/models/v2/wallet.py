"""Wallet model - Logical wallet abstraction."""

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class WalletType(str, enum.Enum):
    """Wallet type enumeration."""
    MULTISIG_POLICY = "MULTISIG_POLICY"
    SINGLE_SIG = "SINGLE_SIG"
    MPC_MANAGED = "MPC_MANAGED"
    EXTERNAL_DESCRIPTOR = "EXTERNAL_DESCRIPTOR"


class WalletStatus(str, enum.Enum):
    """Wallet status enumeration."""
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    COMPROMISED = "COMPROMISED"
    DEPRECATED = "DEPRECATED"


class Wallet(Base):
    """Wallet model - logical wallet for estate plans."""

    __tablename__ = "wallets"

    wallet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estate_plan_id = Column(UUID(as_uuid=True), ForeignKey("estate_plans_v2.estate_plan_id", ondelete="CASCADE"), nullable=False)
    network_id = Column(UUID(as_uuid=True), ForeignKey("networks.network_id"), nullable=False)
    wallet_name = Column(String(255), nullable=False)
    wallet_type = Column(SQLEnum(WalletType), nullable=False)
    descriptor = Column(String(2000), nullable=True)  # Miniscript or output descriptor
    is_inheritance_wallet = Column(Boolean, default=False, nullable=False)
    status = Column(SQLEnum(WalletStatus), default=WalletStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    estate_plan = relationship("EstatePlanV2", back_populates="wallets")
    network = relationship("Network", back_populates="wallets")
    policy_versions = relationship("WalletPolicyVersion", back_populates="wallet", cascade="all, delete-orphan")

