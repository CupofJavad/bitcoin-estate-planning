"""Business logic for Assets & Wallet Policy Service."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.v2.network import Network
from app.models.v2.wallet import Wallet
from app.models.v2.wallet_policy_version import WalletPolicyVersion
from app.models.v2.script_template import ScriptTemplate
from app.models.v2.timelock_config import TimelockConfig
from app.awps.schemas import (
    NetworkCreate, NetworkResponse,
    WalletCreate, WalletUpdate, WalletResponse, WalletWithRelations,
    ScriptTemplateCreate, ScriptTemplateResponse,
    WalletPolicyVersionCreate, WalletPolicyVersionResponse, WalletPolicyVersionWithRelations,
    TimelockConfigCreate, TimelockConfigUpdate, TimelockConfigResponse,
)


class NetworkService:
    """Service for network management."""

    @staticmethod
    async def create_network(db: AsyncSession, network_data: NetworkCreate) -> NetworkResponse:
        """Create a new network."""
        network = Network(**network_data.model_dump())
        db.add(network)
        await db.commit()
        await db.refresh(network)
        return NetworkResponse.model_validate(network)

    @staticmethod
    async def get_network(db: AsyncSession, network_id: UUID) -> Optional[NetworkResponse]:
        """Get a network by ID."""
        result = await db.execute(select(Network).where(Network.network_id == network_id))
        network = result.scalar_one_or_none()
        if not network:
            return None
        return NetworkResponse.model_validate(network)

    @staticmethod
    async def list_networks(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[NetworkResponse]:
        """List networks."""
        result = await db.execute(select(Network).offset(skip).limit(limit))
        networks = result.scalars().all()
        return [NetworkResponse.model_validate(n) for n in networks]


class WalletService:
    """Service for wallet management."""

    @staticmethod
    async def create_wallet(db: AsyncSession, wallet_data: WalletCreate) -> WalletResponse:
        """Create a new wallet."""
        wallet = Wallet(**wallet_data.model_dump())
        db.add(wallet)
        await db.commit()
        await db.refresh(wallet)
        return WalletResponse.model_validate(wallet)

    @staticmethod
    async def get_wallet(db: AsyncSession, wallet_id: UUID) -> Optional[WalletResponse]:
        """Get a wallet by ID."""
        result = await db.execute(select(Wallet).where(Wallet.wallet_id == wallet_id))
        wallet = result.scalar_one_or_none()
        if not wallet:
            return None
        return WalletResponse.model_validate(wallet)

    @staticmethod
    async def get_wallet_with_relations(db: AsyncSession, wallet_id: UUID) -> Optional[WalletWithRelations]:
        """Get a wallet with all relations."""
        result = await db.execute(
            select(Wallet)
            .where(Wallet.wallet_id == wallet_id)
            .options(selectinload(Wallet.policy_versions))
        )
        wallet = result.scalar_one_or_none()
        if not wallet:
            return None
        return WalletWithRelations.model_validate(wallet)

    @staticmethod
    async def list_wallets(db: AsyncSession, estate_plan_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[WalletResponse]:
        """List wallets."""
        query = select(Wallet)
        if estate_plan_id:
            query = query.where(Wallet.estate_plan_id == estate_plan_id)
        result = await db.execute(query.offset(skip).limit(limit))
        wallets = result.scalars().all()
        return [WalletResponse.model_validate(w) for w in wallets]

    @staticmethod
    async def update_wallet(db: AsyncSession, wallet_id: UUID, wallet_data: WalletUpdate) -> Optional[WalletResponse]:
        """Update a wallet."""
        update_data = wallet_data.model_dump(exclude_unset=True)
        if not update_data:
            return await WalletService.get_wallet(db, wallet_id)

        await db.execute(
            update(Wallet)
            .where(Wallet.wallet_id == wallet_id)
            .values(**update_data)
        )
        await db.commit()
        return await WalletService.get_wallet(db, wallet_id)

    @staticmethod
    async def delete_wallet(db: AsyncSession, wallet_id: UUID) -> bool:
        """Delete a wallet."""
        result = await db.execute(delete(Wallet).where(Wallet.wallet_id == wallet_id))
        await db.commit()
        return result.rowcount > 0


class ScriptTemplateService:
    """Service for script template management."""

    @staticmethod
    async def create_template(db: AsyncSession, template_data: ScriptTemplateCreate) -> ScriptTemplateResponse:
        """Create a new script template."""
        template = ScriptTemplate(**template_data.model_dump())
        db.add(template)
        await db.commit()
        await db.refresh(template)
        return ScriptTemplateResponse.model_validate(template)

    @staticmethod
    async def get_template(db: AsyncSession, template_id: UUID) -> Optional[ScriptTemplateResponse]:
        """Get a script template by ID."""
        result = await db.execute(select(ScriptTemplate).where(ScriptTemplate.script_template_id == template_id))
        template = result.scalar_one_or_none()
        if not template:
            return None
        return ScriptTemplateResponse.model_validate(template)

    @staticmethod
    async def list_templates(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ScriptTemplateResponse]:
        """List script templates."""
        result = await db.execute(select(ScriptTemplate).offset(skip).limit(limit))
        templates = result.scalars().all()
        return [ScriptTemplateResponse.model_validate(t) for t in templates]


class WalletPolicyVersionService:
    """Service for wallet policy version management."""

    @staticmethod
    async def create_policy_version(db: AsyncSession, version_data: WalletPolicyVersionCreate) -> WalletPolicyVersionResponse:
        """Create a new wallet policy version."""
        version = WalletPolicyVersion(**version_data.model_dump())
        db.add(version)
        await db.commit()
        await db.refresh(version)
        return WalletPolicyVersionResponse.model_validate(version)

    @staticmethod
    async def get_policy_version(db: AsyncSession, version_id: UUID) -> Optional[WalletPolicyVersionResponse]:
        """Get a wallet policy version by ID."""
        result = await db.execute(select(WalletPolicyVersion).where(WalletPolicyVersion.wallet_policy_version_id == version_id))
        version = result.scalar_one_or_none()
        if not version:
            return None
        return WalletPolicyVersionResponse.model_validate(version)

    @staticmethod
    async def get_policy_version_with_relations(db: AsyncSession, version_id: UUID) -> Optional[WalletPolicyVersionWithRelations]:
        """Get a wallet policy version with all relations."""
        result = await db.execute(
            select(WalletPolicyVersion)
            .where(WalletPolicyVersion.wallet_policy_version_id == version_id)
            .options(selectinload(WalletPolicyVersion.timelock_configs))
        )
        version = result.scalar_one_or_none()
        if not version:
            return None
        return WalletPolicyVersionWithRelations.model_validate(version)

    @staticmethod
    async def get_versions_for_wallet(db: AsyncSession, wallet_id: UUID) -> List[WalletPolicyVersionResponse]:
        """Get all policy versions for a wallet."""
        result = await db.execute(
            select(WalletPolicyVersion)
            .where(WalletPolicyVersion.wallet_id == wallet_id)
            .order_by(WalletPolicyVersion.version_number.desc())
        )
        versions = result.scalars().all()
        return [WalletPolicyVersionResponse.model_validate(v) for v in versions]


class TimelockConfigService:
    """Service for timelock config management."""

    @staticmethod
    async def create_timelock_config(db: AsyncSession, config_data: TimelockConfigCreate) -> TimelockConfigResponse:
        """Create a new timelock config."""
        config = TimelockConfig(**config_data.model_dump())
        db.add(config)
        await db.commit()
        await db.refresh(config)
        return TimelockConfigResponse.model_validate(config)

    @staticmethod
    async def get_timelock_config(db: AsyncSession, config_id: UUID) -> Optional[TimelockConfigResponse]:
        """Get a timelock config by ID."""
        result = await db.execute(select(TimelockConfig).where(TimelockConfig.timelock_config_id == config_id))
        config = result.scalar_one_or_none()
        if not config:
            return None
        return TimelockConfigResponse.model_validate(config)

    @staticmethod
    async def get_configs_for_policy_version(db: AsyncSession, policy_version_id: UUID) -> List[TimelockConfigResponse]:
        """Get all timelock configs for a policy version."""
        result = await db.execute(
            select(TimelockConfig).where(TimelockConfig.wallet_policy_version_id == policy_version_id)
        )
        configs = result.scalars().all()
        return [TimelockConfigResponse.model_validate(c) for c in configs]

    @staticmethod
    async def update_timelock_config(db: AsyncSession, config_id: UUID, config_data: TimelockConfigUpdate) -> Optional[TimelockConfigResponse]:
        """Update a timelock config."""
        update_data = config_data.model_dump(exclude_unset=True)
        if not update_data:
            return await TimelockConfigService.get_timelock_config(db, config_id)

        await db.execute(
            update(TimelockConfig)
            .where(TimelockConfig.timelock_config_id == config_id)
            .values(**update_data)
        )
        await db.commit()
        return await TimelockConfigService.get_timelock_config(db, config_id)

    @staticmethod
    async def delete_timelock_config(db: AsyncSession, config_id: UUID) -> bool:
        """Delete a timelock config."""
        result = await db.execute(delete(TimelockConfig).where(TimelockConfig.timelock_config_id == config_id))
        await db.commit()
        return result.rowcount > 0

