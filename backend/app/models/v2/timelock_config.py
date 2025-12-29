"""TimelockConfig model - Enhanced timelock configuration."""

from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class LockType(str, enum.Enum):
    """Lock type enumeration."""
    ABSOLUTE = "ABSOLUTE"
    RELATIVE = "RELATIVE"


class TimelockConfig(Base):
    """TimelockConfig model - enhanced timelock configuration."""

    __tablename__ = "timelock_configs"

    timelock_config_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_policy_version_id = Column(UUID(as_uuid=True), ForeignKey("wallet_policy_versions.wallet_policy_version_id", ondelete="CASCADE"), nullable=False)
    lock_type = Column(SQLEnum(LockType), nullable=False)
    absolute_block_height = Column(BigInteger, nullable=True)
    absolute_timestamp = Column(DateTime(timezone=True), nullable=True)
    relative_blocks = Column(BigInteger, nullable=True)
    relative_days = Column(Integer, nullable=True)
    primary_path_delay_days = Column(Integer, nullable=True)  # Time before inheritance path can activate
    heir_path_delay_days = Column(Integer, nullable=True)
    backup_path_delay_days = Column(Integer, nullable=True)
    refresh_threshold_days = Column(Integer, nullable=True)  # When to initiate migration
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    wallet_policy_version = relationship("WalletPolicyVersion", back_populates="timelock_configs")

