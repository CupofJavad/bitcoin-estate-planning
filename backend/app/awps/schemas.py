"""Pydantic schemas for Assets & Wallet Policy Service."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.v2.wallet import WalletType, WalletStatus
from app.models.v2.wallet_policy_version import PolicyLanguage, PolicyVersionStatus
from app.models.v2.timelock_config import LockType


# Network Schemas
class NetworkBase(BaseModel):
    """Base network schema."""
    network_type: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    rpc_endpoint_ref: Optional[Dict[str, Any]] = None
    chain_id: Optional[str] = Field(None, max_length=50)


class NetworkCreate(NetworkBase):
    """Schema for creating a network."""
    pass


class NetworkResponse(NetworkBase):
    """Schema for network response."""
    network_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Wallet Schemas
class WalletBase(BaseModel):
    """Base wallet schema."""
    wallet_name: str = Field(..., max_length=255)
    wallet_type: WalletType
    descriptor: Optional[str] = Field(None, max_length=2000)
    is_inheritance_wallet: bool = False
    status: WalletStatus = WalletStatus.ACTIVE


class WalletCreate(WalletBase):
    """Schema for creating a wallet."""
    estate_plan_id: UUID
    network_id: UUID


class WalletUpdate(BaseModel):
    """Schema for updating a wallet."""
    wallet_name: Optional[str] = Field(None, max_length=255)
    descriptor: Optional[str] = Field(None, max_length=2000)
    is_inheritance_wallet: Optional[bool] = None
    status: Optional[WalletStatus] = None


class WalletResponse(WalletBase):
    """Schema for wallet response."""
    wallet_id: UUID
    estate_plan_id: UUID
    network_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Script Template Schemas
class ScriptTemplateBase(BaseModel):
    """Base script template schema."""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    policy_language: str = Field(..., max_length=50)
    policy_template_text: str
    default_parameters: Optional[Dict[str, Any]] = None
    supports_pqc: bool = False


class ScriptTemplateCreate(ScriptTemplateBase):
    """Schema for creating a script template."""
    pass


class ScriptTemplateResponse(ScriptTemplateBase):
    """Schema for script template response."""
    script_template_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Wallet Policy Version Schemas
class WalletPolicyVersionBase(BaseModel):
    """Base wallet policy version schema."""
    version_number: int
    status: PolicyVersionStatus
    policy_language: PolicyLanguage
    policy_text: Optional[str] = None
    script_template_id: Optional[UUID] = None
    effective_from: datetime
    effective_to: Optional[datetime] = None
    upgrade_reason: Optional[str] = None


class WalletPolicyVersionCreate(WalletPolicyVersionBase):
    """Schema for creating a wallet policy version."""
    wallet_id: UUID


class WalletPolicyVersionResponse(WalletPolicyVersionBase):
    """Schema for wallet policy version response."""
    wallet_policy_version_id: UUID
    wallet_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Timelock Config Schemas
class TimelockConfigBase(BaseModel):
    """Base timelock config schema."""
    lock_type: LockType
    absolute_block_height: Optional[int] = None
    absolute_timestamp: Optional[datetime] = None
    relative_blocks: Optional[int] = None
    relative_days: Optional[int] = None
    primary_path_delay_days: Optional[int] = None
    heir_path_delay_days: Optional[int] = None
    backup_path_delay_days: Optional[int] = None
    refresh_threshold_days: Optional[int] = None


class TimelockConfigCreate(TimelockConfigBase):
    """Schema for creating a timelock config."""
    wallet_policy_version_id: UUID


class TimelockConfigUpdate(BaseModel):
    """Schema for updating a timelock config."""
    lock_type: Optional[LockType] = None
    absolute_block_height: Optional[int] = None
    absolute_timestamp: Optional[datetime] = None
    relative_blocks: Optional[int] = None
    relative_days: Optional[int] = None
    primary_path_delay_days: Optional[int] = None
    heir_path_delay_days: Optional[int] = None
    backup_path_delay_days: Optional[int] = None
    refresh_threshold_days: Optional[int] = None


class TimelockConfigResponse(TimelockConfigBase):
    """Schema for timelock config response."""
    timelock_config_id: UUID
    wallet_policy_version_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Wallet with Relations
class WalletWithRelations(WalletResponse):
    """Wallet with all relations."""
    policy_versions: List[WalletPolicyVersionResponse] = []

    class Config:
        from_attributes = True


# Wallet Policy Version with Relations
class WalletPolicyVersionWithRelations(WalletPolicyVersionResponse):
    """Wallet policy version with all relations."""
    timelock_configs: List[TimelockConfigResponse] = []

    class Config:
        from_attributes = True

