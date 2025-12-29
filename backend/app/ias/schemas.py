"""Pydantic schemas for Identity & Access Service."""

from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from app.models.v2.party import PartyType, PartyStatus
from app.models.v2.party_role import RoleType
from app.models.v2.contact_info import ContactType
from app.models.v2.account import AccountStatus
from app.models.v2.auth_credential import CredentialType
from app.models.v2.device import DeviceType


# Party Schemas
class PartyBase(BaseModel):
    """Base party schema."""
    party_type: PartyType
    legal_name: str = Field(..., max_length=500)
    preferred_name: Optional[str] = Field(None, max_length=500)
    date_of_birth: Optional[date] = None
    date_of_incorporation: Optional[date] = None
    tax_id: Optional[str] = Field(None, max_length=100)
    primary_residence_country: Optional[str] = Field(None, max_length=2)
    primary_residence_region: Optional[str] = Field(None, max_length=100)
    primary_residence_city: Optional[str] = Field(None, max_length=100)
    status: PartyStatus = PartyStatus.ACTIVE


class PartyCreate(PartyBase):
    """Schema for creating a party."""
    pass


class PartyUpdate(BaseModel):
    """Schema for updating a party."""
    legal_name: Optional[str] = Field(None, max_length=500)
    preferred_name: Optional[str] = Field(None, max_length=500)
    date_of_birth: Optional[date] = None
    date_of_incorporation: Optional[date] = None
    tax_id: Optional[str] = Field(None, max_length=100)
    primary_residence_country: Optional[str] = Field(None, max_length=2)
    primary_residence_region: Optional[str] = Field(None, max_length=100)
    primary_residence_city: Optional[str] = Field(None, max_length=100)
    status: Optional[PartyStatus] = None


class PartyResponse(PartyBase):
    """Schema for party response."""
    party_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Party Role Schemas
class PartyRoleBase(BaseModel):
    """Base party role schema."""
    role_type: RoleType
    effective_from: date
    effective_to: Optional[date] = None


class PartyRoleCreate(PartyRoleBase):
    """Schema for creating a party role."""
    party_id: UUID


class PartyRoleResponse(PartyRoleBase):
    """Schema for party role response."""
    party_role_id: UUID
    party_id: UUID

    class Config:
        from_attributes = True


# Contact Info Schemas
class ContactInfoBase(BaseModel):
    """Base contact info schema."""
    contact_type: ContactType
    value: str = Field(..., max_length=500)
    is_primary: bool = False


class ContactInfoCreate(ContactInfoBase):
    """Schema for creating contact info."""
    party_id: UUID


class ContactInfoResponse(ContactInfoBase):
    """Schema for contact info response."""
    contact_id: UUID
    party_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Account Schemas
class AccountBase(BaseModel):
    """Base account schema."""
    username: str = Field(..., max_length=255)
    email: EmailStr
    status: AccountStatus = AccountStatus.ACTIVE


class AccountCreate(AccountBase):
    """Schema for creating an account."""
    party_id: UUID
    password: Optional[str] = None


class AccountUpdate(BaseModel):
    """Schema for updating an account."""
    username: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    status: Optional[AccountStatus] = None


class AccountResponse(AccountBase):
    """Schema for account response."""
    account_id: UUID
    party_id: UUID
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Device Schemas
class DeviceBase(BaseModel):
    """Base device schema."""
    device_fingerprint: str = Field(..., max_length=255)
    device_type: DeviceType
    os: Optional[str] = Field(None, max_length=100)
    trusted: bool = False


class DeviceCreate(DeviceBase):
    """Schema for creating a device."""
    party_id: UUID


class DeviceUpdate(BaseModel):
    """Schema for updating a device."""
    device_type: Optional[DeviceType] = None
    os: Optional[str] = Field(None, max_length=100)
    trusted: Optional[bool] = None


class DeviceResponse(DeviceBase):
    """Schema for device response."""
    device_id: UUID
    party_id: UUID
    last_seen_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Party with Relations
class PartyWithRelations(PartyResponse):
    """Party with all relations."""
    roles: List[PartyRoleResponse] = []
    contact_info: List[ContactInfoResponse] = []
    accounts: List[AccountResponse] = []
    devices: List[DeviceResponse] = []

    class Config:
        from_attributes = True

