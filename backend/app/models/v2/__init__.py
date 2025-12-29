"""V2 Models - Enhanced data model for enterprise estate planning."""

# Party & Identity
from app.models.v2.party import Party
from app.models.v2.party_role import PartyRole
from app.models.v2.contact_info import ContactInfo
from app.models.v2.account import Account
from app.models.v2.auth_credential import AuthCredential
from app.models.v2.device import Device

# Estate Planning
from app.models.v2.jurisdiction import Jurisdiction
from app.models.v2.estate_plan import EstatePlanV2
from app.models.v2.estate_plan_version import EstatePlanVersion
from app.models.v2.estate_plan_participant import EstatePlanParticipant
from app.models.v2.beneficiary_allocation import BeneficiaryAllocation
from app.models.v2.legal_document import LegalDocument
from app.models.v2.life_event import LifeEvent

# Compliance
from app.models.v2.kyc_case import KYCCase
from app.models.v2.kyc_document import KYCDocument
from app.models.v2.sanctions_screening import SanctionsScreening
from app.models.v2.party_risk_profile import PartyRiskProfile

# Wallet & Policies
from app.models.v2.network import Network
from app.models.v2.wallet import Wallet
from app.models.v2.wallet_policy_version import WalletPolicyVersion
from app.models.v2.script_template import ScriptTemplate
from app.models.v2.timelock_config import TimelockConfig

# Audit & Notifications
from app.models.v2.audit_log import AuditLog
from app.models.v2.notification import Notification, NotificationPreference

__all__ = [
    # Party & Identity
    "Party",
    "PartyRole",
    "ContactInfo",
    "Account",
    "AuthCredential",
    "Device",
    # Estate Planning
    "Jurisdiction",
    "EstatePlanV2",
    "EstatePlanVersion",
    "EstatePlanParticipant",
    "BeneficiaryAllocation",
    "LegalDocument",
    "LifeEvent",
    # Compliance
    "KYCCase",
    "KYCDocument",
    "SanctionsScreening",
    "PartyRiskProfile",
    # Wallet & Policies
    "Network",
    "Wallet",
    "WalletPolicyVersion",
    "ScriptTemplate",
    "TimelockConfig",
    # Audit & Notifications
    "AuditLog",
    "Notification",
    "NotificationPreference",
]

