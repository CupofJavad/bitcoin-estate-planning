"""PartyRole model - Links parties to roles."""

from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class RoleType(str, enum.Enum):
    """Role type enumeration."""
    CLIENT = "CLIENT"
    BENEFICIARY = "BENEFICIARY"
    EXECUTOR = "EXECUTOR"
    ATTORNEY = "ATTORNEY"
    ADVISOR = "ADVISOR"
    STAFF = "STAFF"
    ORACLE_PROVIDER = "ORACLE_PROVIDER"
    INSURANCE_UNDERWRITER = "INSURANCE_UNDERWRITER"
    EXCHANGE_PARTNER = "EXCHANGE_PARTNER"
    CUSTODY_PARTNER = "CUSTODY_PARTNER"


class PartyRole(Base):
    """PartyRole model - links parties to roles."""

    __tablename__ = "party_roles"

    party_role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.party_id", ondelete="CASCADE"), nullable=False)
    role_type = Column(SQLEnum(RoleType), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)

    # Relationships
    party = relationship("Party", back_populates="roles")

