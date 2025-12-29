"""AuthCredential model - Authentication credentials."""

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class CredentialType(str, enum.Enum):
    """Credential type enumeration."""
    PASSWORD = "PASSWORD"
    TOTP = "TOTP"
    FIDO2_PASSKEY = "FIDO2_PASSKEY"
    RECOVERY_CODE = "RECOVERY_CODE"


class AuthCredential(Base):
    """AuthCredential model - authentication credentials."""

    __tablename__ = "auth_credentials"

    auth_credential_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id", ondelete="CASCADE"), nullable=False)
    credential_type = Column(SQLEnum(CredentialType), nullable=False)
    public_key = Column(String(1000), nullable=True)  # For passkeys
    config_data = Column(JSONB, nullable=True)  # TOTP secret metadata, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    account = relationship("Account", back_populates="auth_credentials")

