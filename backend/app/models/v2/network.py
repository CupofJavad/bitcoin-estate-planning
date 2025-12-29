"""Network model - Blockchain networks."""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class NetworkType(str, enum.Enum):
    """Network type enumeration."""
    BITCOIN = "BITCOIN"
    ETHEREUM = "ETHEREUM"
    OTHER = "OTHER"


class Network(Base):
    """Network model - blockchain networks."""

    __tablename__ = "networks"

    network_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network_type = Column(String(50), nullable=False)  # BITCOIN, ETHEREUM, etc.
    name = Column(String(200), nullable=False)  # "Bitcoin mainnet", "Ethereum mainnet"
    rpc_endpoint_ref = Column(JSONB, nullable=True)  # Config for nodes
    chain_id = Column(String(50), nullable=True)  # For EVM chains
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    wallets = relationship("Wallet", back_populates="network")

