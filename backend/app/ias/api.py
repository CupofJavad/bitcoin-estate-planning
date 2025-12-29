"""API endpoints for Identity & Access Service."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.ias.schemas import (
    PartyCreate, PartyUpdate, PartyResponse, PartyWithRelations,
    PartyRoleCreate, PartyRoleResponse,
    ContactInfoCreate, ContactInfoResponse,
    AccountCreate, AccountUpdate, AccountResponse,
    DeviceCreate, DeviceUpdate, DeviceResponse,
)
from app.ias.service import (
    PartyService, PartyRoleService, ContactInfoService,
    AccountService, DeviceService,
)

router = APIRouter(prefix="/v2/ias", tags=["Identity & Access Service"])


# Party endpoints
@router.post("/parties", response_model=PartyResponse, status_code=status.HTTP_201_CREATED)
async def create_party(
    party: PartyCreate,
    db: AsyncSession = Depends(get_db),
) -> PartyResponse:
    """Create a new party."""
    return await PartyService.create_party(db, party)


@router.get("/parties/{party_id}", response_model=PartyResponse)
async def get_party(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> PartyResponse:
    """Get a party by ID."""
    party = await PartyService.get_party(db, party_id)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Party not found"
        )
    return party


@router.get("/parties/{party_id}/full", response_model=PartyWithRelations)
async def get_party_with_relations(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> PartyWithRelations:
    """Get a party with all relations."""
    party = await PartyService.get_party_with_relations(db, party_id)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Party not found"
        )
    return party


@router.get("/parties", response_model=List[PartyResponse])
async def list_parties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> List[PartyResponse]:
    """List parties."""
    return await PartyService.list_parties(db, skip=skip, limit=limit)


@router.patch("/parties/{party_id}", response_model=PartyResponse)
async def update_party(
    party_id: UUID,
    party_update: PartyUpdate,
    db: AsyncSession = Depends(get_db),
) -> PartyResponse:
    """Update a party."""
    party = await PartyService.update_party(db, party_id, party_update)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Party not found"
        )
    return party


@router.delete("/parties/{party_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_party(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a party."""
    deleted = await PartyService.delete_party(db, party_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Party not found"
        )


# Party Role endpoints
@router.post("/parties/{party_id}/roles", response_model=PartyRoleResponse, status_code=status.HTTP_201_CREATED)
async def create_party_role(
    party_id: UUID,
    role: PartyRoleCreate,
    db: AsyncSession = Depends(get_db),
) -> PartyRoleResponse:
    """Create a role for a party."""
    role_data = role.model_dump()
    role_data["party_id"] = party_id
    return await PartyRoleService.create_role(db, PartyRoleCreate(**role_data))


@router.get("/parties/{party_id}/roles", response_model=List[PartyRoleResponse])
async def get_party_roles(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[PartyRoleResponse]:
    """Get all roles for a party."""
    return await PartyRoleService.get_roles_for_party(db, party_id)


# Contact Info endpoints
@router.post("/parties/{party_id}/contact-info", response_model=ContactInfoResponse, status_code=status.HTTP_201_CREATED)
async def create_contact_info(
    party_id: UUID,
    contact: ContactInfoCreate,
    db: AsyncSession = Depends(get_db),
) -> ContactInfoResponse:
    """Create contact info for a party."""
    contact_data = contact.model_dump()
    contact_data["party_id"] = party_id
    return await ContactInfoService.create_contact_info(db, ContactInfoCreate(**contact_data))


@router.get("/parties/{party_id}/contact-info", response_model=List[ContactInfoResponse])
async def get_party_contact_info(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[ContactInfoResponse]:
    """Get all contact info for a party."""
    return await ContactInfoService.get_contact_info_for_party(db, party_id)


# Account endpoints
@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account: AccountCreate,
    db: AsyncSession = Depends(get_db),
) -> AccountResponse:
    """Create a new account."""
    return await AccountService.create_account(db, account)


@router.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> AccountResponse:
    """Get an account by ID."""
    account = await AccountService.get_account(db, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account


# Device endpoints
@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_device(
    device: DeviceCreate,
    db: AsyncSession = Depends(get_db),
) -> DeviceResponse:
    """Create or update a device."""
    return await DeviceService.create_or_update_device(db, device)


@router.get("/parties/{party_id}/devices", response_model=List[DeviceResponse])
async def get_party_devices(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[DeviceResponse]:
    """Get all devices for a party."""
    return await DeviceService.get_devices_for_party(db, party_id)

