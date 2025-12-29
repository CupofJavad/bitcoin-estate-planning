"""Business logic for Identity & Access Service."""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.v2.party import Party
from app.models.v2.party_role import PartyRole
from app.models.v2.contact_info import ContactInfo
from app.models.v2.account import Account
from app.models.v2.device import Device
from app.ias.schemas import (
    PartyCreate, PartyUpdate, PartyResponse,
    PartyRoleCreate, PartyRoleResponse,
    ContactInfoCreate, ContactInfoResponse,
    AccountCreate, AccountUpdate, AccountResponse,
    DeviceCreate, DeviceUpdate, DeviceResponse,
    PartyWithRelations,
)


class PartyService:
    """Service for party management."""

    @staticmethod
    async def create_party(db: AsyncSession, party_data: PartyCreate) -> PartyResponse:
        """Create a new party."""
        party = Party(**party_data.model_dump())
        db.add(party)
        await db.commit()
        await db.refresh(party)
        return PartyResponse.model_validate(party)

    @staticmethod
    async def get_party(db: AsyncSession, party_id: UUID) -> Optional[PartyResponse]:
        """Get a party by ID."""
        result = await db.execute(select(Party).where(Party.party_id == party_id))
        party = result.scalar_one_or_none()
        if not party:
            return None
        return PartyResponse.model_validate(party)

    @staticmethod
    async def get_party_with_relations(db: AsyncSession, party_id: UUID) -> Optional[PartyWithRelations]:
        """Get a party with all relations."""
        result = await db.execute(
            select(Party)
            .where(Party.party_id == party_id)
            .options(
                selectinload(Party.roles),
                selectinload(Party.contact_info),
                selectinload(Party.accounts),
                selectinload(Party.devices),
            )
        )
        party = result.scalar_one_or_none()
        if not party:
            return None
        return PartyWithRelations.model_validate(party)

    @staticmethod
    async def list_parties(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[PartyResponse]:
        """List parties."""
        result = await db.execute(select(Party).offset(skip).limit(limit))
        parties = result.scalars().all()
        return [PartyResponse.model_validate(p) for p in parties]

    @staticmethod
    async def update_party(db: AsyncSession, party_id: UUID, party_data: PartyUpdate) -> Optional[PartyResponse]:
        """Update a party."""
        update_data = party_data.model_dump(exclude_unset=True)
        if not update_data:
            return await PartyService.get_party(db, party_id)

        await db.execute(
            update(Party)
            .where(Party.party_id == party_id)
            .values(**update_data)
        )
        await db.commit()
        return await PartyService.get_party(db, party_id)

    @staticmethod
    async def delete_party(db: AsyncSession, party_id: UUID) -> bool:
        """Delete a party."""
        result = await db.execute(delete(Party).where(Party.party_id == party_id))
        await db.commit()
        return result.rowcount > 0


class PartyRoleService:
    """Service for party role management."""

    @staticmethod
    async def create_role(db: AsyncSession, role_data: PartyRoleCreate) -> PartyRoleResponse:
        """Create a new party role."""
        role = PartyRole(**role_data.model_dump())
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return PartyRoleResponse.model_validate(role)

    @staticmethod
    async def get_roles_for_party(db: AsyncSession, party_id: UUID) -> List[PartyRoleResponse]:
        """Get all roles for a party."""
        result = await db.execute(select(PartyRole).where(PartyRole.party_id == party_id))
        roles = result.scalars().all()
        return [PartyRoleResponse.model_validate(r) for r in roles]


class ContactInfoService:
    """Service for contact info management."""

    @staticmethod
    async def create_contact_info(db: AsyncSession, contact_data: ContactInfoCreate) -> ContactInfoResponse:
        """Create new contact info."""
        contact = ContactInfo(**contact_data.model_dump())
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return ContactInfoResponse.model_validate(contact)

    @staticmethod
    async def get_contact_info_for_party(db: AsyncSession, party_id: UUID) -> List[ContactInfoResponse]:
        """Get all contact info for a party."""
        result = await db.execute(select(ContactInfo).where(ContactInfo.party_id == party_id))
        contacts = result.scalars().all()
        return [ContactInfoResponse.model_validate(c) for c in contacts]


class AccountService:
    """Service for account management."""

    @staticmethod
    async def create_account(db: AsyncSession, account_data: AccountCreate) -> AccountResponse:
        """Create a new account."""
        account_dict = account_data.model_dump(exclude={"password"})
        account = Account(**account_dict)
        # TODO: Hash password if provided
        if account_data.password:
            # account.password_hash = hash_password(account_data.password)
            pass
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return AccountResponse.model_validate(account)

    @staticmethod
    async def get_account(db: AsyncSession, account_id: UUID) -> Optional[AccountResponse]:
        """Get an account by ID."""
        result = await db.execute(select(Account).where(Account.account_id == account_id))
        account = result.scalar_one_or_none()
        if not account:
            return None
        return AccountResponse.model_validate(account)

    @staticmethod
    async def get_account_by_username(db: AsyncSession, username: str) -> Optional[AccountResponse]:
        """Get an account by username."""
        result = await db.execute(select(Account).where(Account.username == username))
        account = result.scalar_one_or_none()
        if not account:
            return None
        return AccountResponse.model_validate(account)


class DeviceService:
    """Service for device management."""

    @staticmethod
    async def create_or_update_device(db: AsyncSession, device_data: DeviceCreate) -> DeviceResponse:
        """Create or update a device (by fingerprint)."""
        result = await db.execute(
            select(Device).where(Device.device_fingerprint == device_data.device_fingerprint)
        )
        device = result.scalar_one_or_none()
        
        if device:
            # Update existing device
            for key, value in device_data.model_dump(exclude={"party_id", "device_fingerprint"}).items():
                setattr(device, key, value)
            device.last_seen_at = datetime.utcnow()
        else:
            # Create new device
            device = Device(**device_data.model_dump())
            db.add(device)
        
        await db.commit()
        await db.refresh(device)
        return DeviceResponse.model_validate(device)

    @staticmethod
    async def get_devices_for_party(db: AsyncSession, party_id: UUID) -> List[DeviceResponse]:
        """Get all devices for a party."""
        result = await db.execute(select(Device).where(Device.party_id == party_id))
        devices = result.scalars().all()
        return [DeviceResponse.model_validate(d) for d in devices]

