"""API endpoints for Assets & Wallet Policy Service."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.awps.schemas import (
    NetworkCreate, NetworkResponse,
    WalletCreate, WalletUpdate, WalletResponse, WalletWithRelations,
    ScriptTemplateCreate, ScriptTemplateResponse,
    WalletPolicyVersionCreate, WalletPolicyVersionResponse, WalletPolicyVersionWithRelations,
    TimelockConfigCreate, TimelockConfigUpdate, TimelockConfigResponse,
)
from app.awps.service import (
    NetworkService, WalletService, ScriptTemplateService,
    WalletPolicyVersionService, TimelockConfigService,
)

router = APIRouter(prefix="/v2/awps", tags=["Assets & Wallet Policy Service"])


# Network endpoints
@router.post("/networks", response_model=NetworkResponse, status_code=status.HTTP_201_CREATED)
async def create_network(
    network: NetworkCreate,
    db: AsyncSession = Depends(get_db),
) -> NetworkResponse:
    """Create a new network."""
    return await NetworkService.create_network(db, network)


@router.get("/networks/{network_id}", response_model=NetworkResponse)
async def get_network(
    network_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> NetworkResponse:
    """Get a network by ID."""
    network = await NetworkService.get_network(db, network_id)
    if not network:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Network not found"
        )
    return network


@router.get("/networks", response_model=List[NetworkResponse])
async def list_networks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> List[NetworkResponse]:
    """List networks."""
    return await NetworkService.list_networks(db, skip=skip, limit=limit)


# Wallet endpoints
@router.post("/wallets", response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
async def create_wallet(
    wallet: WalletCreate,
    db: AsyncSession = Depends(get_db),
) -> WalletResponse:
    """Create a new wallet."""
    return await WalletService.create_wallet(db, wallet)


@router.get("/wallets/{wallet_id}", response_model=WalletResponse)
async def get_wallet(
    wallet_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> WalletResponse:
    """Get a wallet by ID."""
    wallet = await WalletService.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    return wallet


@router.get("/wallets/{wallet_id}/full", response_model=WalletWithRelations)
async def get_wallet_with_relations(
    wallet_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> WalletWithRelations:
    """Get a wallet with all relations."""
    wallet = await WalletService.get_wallet_with_relations(db, wallet_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    return wallet


@router.get("/wallets", response_model=List[WalletResponse])
async def list_wallets(
    estate_plan_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> List[WalletResponse]:
    """List wallets."""
    return await WalletService.list_wallets(db, estate_plan_id=estate_plan_id, skip=skip, limit=limit)


@router.patch("/wallets/{wallet_id}", response_model=WalletResponse)
async def update_wallet(
    wallet_id: UUID,
    wallet_update: WalletUpdate,
    db: AsyncSession = Depends(get_db),
) -> WalletResponse:
    """Update a wallet."""
    wallet = await WalletService.update_wallet(db, wallet_id, wallet_update)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    return wallet


@router.delete("/wallets/{wallet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wallet(
    wallet_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a wallet."""
    deleted = await WalletService.delete_wallet(db, wallet_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )


# Script Template endpoints
@router.post("/script-templates", response_model=ScriptTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_script_template(
    template: ScriptTemplateCreate,
    db: AsyncSession = Depends(get_db),
) -> ScriptTemplateResponse:
    """Create a new script template."""
    return await ScriptTemplateService.create_template(db, template)


@router.get("/script-templates/{template_id}", response_model=ScriptTemplateResponse)
async def get_script_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ScriptTemplateResponse:
    """Get a script template by ID."""
    template = await ScriptTemplateService.get_template(db, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script template not found"
        )
    return template


@router.get("/script-templates", response_model=List[ScriptTemplateResponse])
async def list_script_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> List[ScriptTemplateResponse]:
    """List script templates."""
    return await ScriptTemplateService.list_templates(db, skip=skip, limit=limit)


# Wallet Policy Version endpoints
@router.post("/wallets/{wallet_id}/policy-versions", response_model=WalletPolicyVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_policy_version(
    wallet_id: UUID,
    version: WalletPolicyVersionCreate,
    db: AsyncSession = Depends(get_db),
) -> WalletPolicyVersionResponse:
    """Create a new policy version for a wallet."""
    version_data = version.model_dump()
    version_data["wallet_id"] = wallet_id
    return await WalletPolicyVersionService.create_policy_version(db, WalletPolicyVersionCreate(**version_data))


@router.get("/policy-versions/{version_id}", response_model=WalletPolicyVersionResponse)
async def get_policy_version(
    version_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> WalletPolicyVersionResponse:
    """Get a policy version by ID."""
    version = await WalletPolicyVersionService.get_policy_version(db, version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy version not found"
        )
    return version


@router.get("/policy-versions/{version_id}/full", response_model=WalletPolicyVersionWithRelations)
async def get_policy_version_with_relations(
    version_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> WalletPolicyVersionWithRelations:
    """Get a policy version with all relations."""
    version = await WalletPolicyVersionService.get_policy_version_with_relations(db, version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy version not found"
        )
    return version


@router.get("/wallets/{wallet_id}/policy-versions", response_model=List[WalletPolicyVersionResponse])
async def get_policy_versions_for_wallet(
    wallet_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[WalletPolicyVersionResponse]:
    """Get all policy versions for a wallet."""
    return await WalletPolicyVersionService.get_versions_for_wallet(db, wallet_id)


# Timelock Config endpoints
@router.post("/policy-versions/{policy_version_id}/timelock-configs", response_model=TimelockConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_timelock_config(
    policy_version_id: UUID,
    config: TimelockConfigCreate,
    db: AsyncSession = Depends(get_db),
) -> TimelockConfigResponse:
    """Create a new timelock config for a policy version."""
    config_data = config.model_dump()
    config_data["wallet_policy_version_id"] = policy_version_id
    return await TimelockConfigService.create_timelock_config(db, TimelockConfigCreate(**config_data))


@router.get("/timelock-configs/{config_id}", response_model=TimelockConfigResponse)
async def get_timelock_config(
    config_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> TimelockConfigResponse:
    """Get a timelock config by ID."""
    config = await TimelockConfigService.get_timelock_config(db, config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timelock config not found"
        )
    return config


@router.get("/policy-versions/{policy_version_id}/timelock-configs", response_model=List[TimelockConfigResponse])
async def get_timelock_configs_for_policy_version(
    policy_version_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[TimelockConfigResponse]:
    """Get all timelock configs for a policy version."""
    return await TimelockConfigService.get_configs_for_policy_version(db, policy_version_id)


@router.patch("/timelock-configs/{config_id}", response_model=TimelockConfigResponse)
async def update_timelock_config(
    config_id: UUID,
    config_update: TimelockConfigUpdate,
    db: AsyncSession = Depends(get_db),
) -> TimelockConfigResponse:
    """Update a timelock config."""
    config = await TimelockConfigService.update_timelock_config(db, config_id, config_update)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timelock config not found"
        )
    return config


@router.delete("/timelock-configs/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timelock_config(
    config_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a timelock config."""
    deleted = await TimelockConfigService.delete_timelock_config(db, config_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timelock config not found"
        )

