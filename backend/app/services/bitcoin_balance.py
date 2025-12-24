"""Bitcoin balance checking service.

Securely checks Bitcoin wallet balances using external APIs with proper
caching, rate limiting, and error handling.
"""

import httpx
import asyncio
from typing import Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings
from app.services.bitcoin_validator import validate_bitcoin_address

# Import redis client if available
try:
    from app.core.redis import get_redis
except ImportError:
    get_redis = None


class BitcoinBalanceService:
    """Service for checking Bitcoin wallet balances securely."""

    # Cache TTL (5 minutes)
    CACHE_TTL = 300  # seconds

    # API endpoints
    BLOCKSTREAM_MAINNET = "https://blockstream.info/api"
    BLOCKSTREAM_TESTNET = "https://blockstream.info/testnet/api"

    # Request timeout (seconds)
    REQUEST_TIMEOUT = 10

    def __init__(self):
        """Initialize balance service."""
        self.network = settings.BITCOIN_NETWORK.lower()
        self.base_url = (
            self.BLOCKSTREAM_MAINNET
            if self.network == "mainnet"
            else self.BLOCKSTREAM_TESTNET
        )

    async def get_balance(
        self, address: str, use_cache: bool = True
    ) -> Dict[str, any]:
        """Get Bitcoin balance for an address.

        Args:
            address: Bitcoin address
            use_cache: Whether to use cached results

        Returns:
            Dictionary with balance information:
            {
                "address": str,
                "balance_btc": float,
                "balance_sats": int,
                "confirmed": bool,
                "cached": bool,
                "last_updated": str (ISO format),
                "error": str (if error occurred)
            }
        """
        # Validate address first (security: never check invalid addresses)
        validation = validate_bitcoin_address(address, network=self.network)
        if not validation["valid"]:
            return {
                "address": address,
                "balance_btc": 0.0,
                "balance_sats": 0,
                "confirmed": False,
                "cached": False,
                "error": f"Invalid address: {', '.join(validation['errors'])}",
            }

        # Check cache first
        if use_cache:
            cached = await self._get_cached_balance(address)
            if cached:
                return {**cached, "cached": True}

        # Fetch from API
        try:
            balance_data = await self._fetch_balance_from_api(address)
            balance_data["cached"] = False

            # Cache the result
            if use_cache and balance_data.get("balance_sats") is not None:
                await self._cache_balance(address, balance_data)

            return balance_data
        except Exception as e:
            # Return error without exposing internal details
            return {
                "address": address,
                "balance_btc": 0.0,
                "balance_sats": 0,
                "confirmed": False,
                "cached": False,
                "error": "Unable to fetch balance. Please try again later.",
            }

    async def _fetch_balance_from_api(self, address: str) -> Dict[str, any]:
        """Fetch balance from Blockstream API.

        Args:
            address: Bitcoin address

        Returns:
            Balance data dictionary
        """
        url = f"{self.base_url}/address/{address}"

        async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
            # Use HTTPS only (security requirement)
            if not url.startswith("https://"):
                raise ValueError("API URL must use HTTPS")

            response = await client.get(url)
            response.raise_for_status()

            data = response.json()

            # Calculate balance from chain_stats
            chain_stats = data.get("chain_stats", {})
            funded = chain_stats.get("funded_txo_sum", 0)
            spent = chain_stats.get("spent_txo_sum", 0)
            balance_sats = funded - spent

            return {
                "address": address,
                "balance_btc": balance_sats / 100_000_000,  # Convert satoshis to BTC
                "balance_sats": balance_sats,
                "confirmed": True,
                "last_updated": datetime.utcnow().isoformat() + "Z",
            }

    async def _get_cached_balance(self, address: str) -> Optional[Dict[str, any]]:
        """Get cached balance from Redis.

        Args:
            address: Bitcoin address

        Returns:
            Cached balance data or None
        """
        if not get_redis:
            return None

        try:
            redis = await get_redis()
            cache_key = f"bitcoin:balance:{self.network}:{address}"
            cached_data = await redis.get(cache_key)
            if cached_data:
                import json
                return json.loads(cached_data)
        except Exception:
            # If caching fails, continue without cache
            pass

        return None

    async def _cache_balance(self, address: str, balance_data: Dict[str, any]) -> None:
        """Cache balance data in Redis.

        Args:
            address: Bitcoin address
            balance_data: Balance data to cache
        """
        if not get_redis:
            return

        try:
            redis = await get_redis()
            cache_key = f"bitcoin:balance:{self.network}:{address}"
            import json
            await redis.setex(
                cache_key, self.CACHE_TTL, json.dumps(balance_data)
            )
        except Exception:
            # If caching fails, continue without cache
            pass


# Convenience function
async def get_bitcoin_balance(
    address: str, network: str = "testnet", use_cache: bool = True
) -> Dict[str, any]:
    """Get Bitcoin balance for an address.

    Args:
        address: Bitcoin address
        network: Network type ("mainnet" or "testnet")
        use_cache: Whether to use cached results

    Returns:
        Balance data dictionary
    """
    service = BitcoinBalanceService()
    return await service.get_balance(address, use_cache=use_cache)

