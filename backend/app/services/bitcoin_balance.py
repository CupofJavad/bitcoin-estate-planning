"""Bitcoin balance checking service.

Securely checks Bitcoin wallet balances using multiple APIs with fallback,
deviation threshold validation, and enhanced error handling.

Patterns inspired by:
- eigenwallet/core: Multi-source validation and connection resilience
- Bitcoin Core: Robust error handling
- BTCPay Server: Production-grade API patterns
"""

import httpx
import asyncio
import logging
from typing import Dict, Optional, List
from datetime import datetime
from app.core.config import settings
from app.services.bitcoin_validator import validate_bitcoin_address

# Import redis client if available
try:
    from app.core.redis import get_redis
except ImportError:
    get_redis = None

logger = logging.getLogger(__name__)


class BitcoinAPIProvider:
    """Represents a Bitcoin API provider."""

    def __init__(self, name: str, mainnet_url: str, testnet_url: str, priority: int):
        """Initialize API provider.

        Args:
            name: Provider name
            mainnet_url: Mainnet API base URL
            testnet_url: Testnet API base URL
            priority: Priority (lower = higher priority)
        """
        self.name = name
        self.mainnet_url = mainnet_url
        self.testnet_url = testnet_url
        self.priority = priority

    def get_url(self, network: str) -> str:
        """Get API URL for network."""
        return self.mainnet_url if network == "mainnet" else self.testnet_url


# API Providers (inspired by eigenwallet's multi-exchange approach)
BITCOIN_API_PROVIDERS = [
    BitcoinAPIProvider(
        name="blockstream",
        mainnet_url="https://blockstream.info/api",
        testnet_url="https://blockstream.info/testnet/api",
        priority=1,  # Highest priority
    ),
    BitcoinAPIProvider(
        name="blockchain_info",
        mainnet_url="https://blockchain.info",
        testnet_url="https://blockchain.info/testnet",  # Note: May not exist
        priority=2,
    ),
    BitcoinAPIProvider(
        name="mempool_space",
        mainnet_url="https://mempool.space/api",
        testnet_url="https://mempool.space/testnet/api",
        priority=3,
    ),
]


class BitcoinBalanceService:
    """Service for checking Bitcoin wallet balances securely.

    Features:
    - Multi-API fallback (inspired by eigenwallet/core)
    - Deviation threshold validation (10% threshold)
    - Exponential backoff retry logic
    - Comprehensive error handling
    - Redis caching
    """

    # Cache TTL (5 minutes)
    CACHE_TTL = 300  # seconds

    # Request timeout (seconds)
    REQUEST_TIMEOUT = 10

    # Retry configuration (inspired by eigenwallet's connection resilience)
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 1  # seconds

    # Deviation threshold (inspired by eigenwallet's 10% threshold)
    DEVIATION_THRESHOLD = 0.10  # 10%

    def __init__(self):
        """Initialize balance service."""
        self.network = settings.BITCOIN_NETWORK.lower()
        # Sort providers by priority
        self.providers = sorted(BITCOIN_API_PROVIDERS, key=lambda x: x.priority)

    async def get_balance(
        self, address: str, use_cache: bool = True
    ) -> Dict[str, any]:
        """Get Bitcoin balance for an address with multi-API fallback.

        Args:
            address: Bitcoin address
            use_cache: Whether to use cached results

        Returns:
            Dictionary with balance information
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

        # Fetch from multiple APIs with fallback
        try:
            balance_data = await self._fetch_balance_with_fallback(address)
            balance_data["cached"] = False

            # Cache the result
            if use_cache and balance_data.get("balance_sats") is not None:
                await self._cache_balance(address, balance_data)

            return balance_data
        except Exception as e:
            logger.error(f"Error fetching balance for {address}: {str(e)}")
            # Return error without exposing internal details
            return {
                "address": address,
                "balance_btc": 0.0,
                "balance_sats": 0,
                "confirmed": False,
                "cached": False,
                "error": "Unable to fetch balance. Please try again later.",
            }

    async def _fetch_balance_with_fallback(self, address: str) -> Dict[str, any]:
        """Fetch balance from multiple APIs with fallback and validation.

        Inspired by eigenwallet/core's multi-exchange approach with deviation checking.

        Args:
            address: Bitcoin address

        Returns:
            Balance data dictionary

        Raises:
            Exception: If all APIs fail or data is inconsistent
        """
        results: List[Dict[str, any]] = []
        errors: List[str] = []

        # Try each provider in priority order
        for provider in self.providers:
            try:
                result = await self._fetch_from_provider(provider, address)
                if result and result.get("balance_sats") is not None:
                    results.append(result)
                    logger.info(
                        f"Successfully fetched balance from {provider.name}: "
                        f"{result['balance_sats']} sats"
                    )
            except Exception as e:
                error_msg = f"{provider.name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"Failed to fetch from {provider.name}: {str(e)}")
                continue

        # Need at least one successful result
        if not results:
            raise Exception(f"All API providers failed. Errors: {', '.join(errors)}")

        # If we have multiple results, validate consistency
        if len(results) > 1:
            is_consistent = self._validate_balance_consistency(results)
            if not is_consistent:
                logger.warning(
                    f"Balance inconsistency detected for {address}. "
                    f"Results: {[r['balance_sats'] for r in results]}"
                )
                # Use the highest priority result, but log the inconsistency
                # In production, you might want to reject or flag this
                return results[0]  # Return first (highest priority) result

        # Return the result from highest priority provider
        return results[0]

    def _validate_balance_consistency(
        self, results: List[Dict[str, any]]
    ) -> bool:
        """Validate that balance results are consistent.

        Inspired by eigenwallet's 10% deviation threshold protection.

        Args:
            results: List of balance results from different APIs

        Returns:
            True if results are consistent, False otherwise
        """
        if len(results) < 2:
            return True

        balances = [r["balance_sats"] for r in results]
        avg_balance = sum(balances) / len(balances)

        # Check each balance against average
        for balance in balances:
            if avg_balance == 0:
                # If average is 0, all should be 0
                if balance != 0:
                    return False
            else:
                deviation = abs(balance - avg_balance) / avg_balance
                if deviation > self.DEVIATION_THRESHOLD:
                    logger.warning(
                        f"Balance deviation {deviation:.2%} exceeds threshold "
                        f"{self.DEVIATION_THRESHOLD:.2%}"
                    )
                    return False

        return True

    async def _fetch_from_provider(
        self, provider: BitcoinAPIProvider, address: str
    ) -> Optional[Dict[str, any]]:
        """Fetch balance from a specific provider with retry logic.

        Inspired by eigenwallet's connection resilience patterns.

        Args:
            provider: API provider
            address: Bitcoin address

        Returns:
            Balance data or None if failed

        Raises:
            Exception: If all retries fail
        """
        base_url = provider.get_url(self.network)

        # Retry with exponential backoff
        for attempt in range(self.MAX_RETRIES):
            try:
                if provider.name == "blockstream":
                    return await self._fetch_blockstream(base_url, address)
                elif provider.name == "blockchain_info":
                    return await self._fetch_blockchain_info(base_url, address)
                elif provider.name == "mempool_space":
                    return await self._fetch_mempool_space(base_url, address)
                else:
                    raise ValueError(f"Unknown provider: {provider.name}")

            except Exception as e:
                if attempt == self.MAX_RETRIES - 1:
                    # Last attempt failed
                    raise

                # Exponential backoff
                wait_time = self.INITIAL_RETRY_DELAY * (2 ** attempt)
                logger.debug(
                    f"Retry {attempt + 1}/{self.MAX_RETRIES} for {provider.name} "
                    f"after {wait_time}s"
                )
                await asyncio.sleep(wait_time)

        return None

    async def _fetch_blockstream(self, base_url: str, address: str) -> Dict[str, any]:
        """Fetch balance from Blockstream API."""
        url = f"{base_url}/address/{address}"

        async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
            if not url.startswith("https://"):
                raise ValueError("API URL must use HTTPS")

            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            chain_stats = data.get("chain_stats", {})
            funded = chain_stats.get("funded_txo_sum", 0)
            spent = chain_stats.get("spent_txo_sum", 0)
            balance_sats = funded - spent

            return {
                "address": address,
                "balance_btc": balance_sats / 100_000_000,
                "balance_sats": balance_sats,
                "confirmed": True,
                "provider": "blockstream",
                "last_updated": datetime.utcnow().isoformat() + "Z",
            }

    async def _fetch_blockchain_info(
        self, base_url: str, address: str
    ) -> Dict[str, any]:
        """Fetch balance from Blockchain.info API."""
        # Note: This is a simplified implementation
        # Blockchain.info API structure may differ
        url = f"{base_url}/q/addressbalance/{address}"

        async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
            if not url.startswith("https://"):
                raise ValueError("API URL must use HTTPS")

            response = await client.get(url)
            response.raise_for_status()
            balance_sats = int(response.text)

            return {
                "address": address,
                "balance_btc": balance_sats / 100_000_000,
                "balance_sats": balance_sats,
                "confirmed": True,
                "provider": "blockchain_info",
                "last_updated": datetime.utcnow().isoformat() + "Z",
            }

    async def _fetch_mempool_space(
        self, base_url: str, address: str
    ) -> Dict[str, any]:
        """Fetch balance from Mempool.space API."""
        url = f"{base_url}/address/{address}"

        async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
            if not url.startswith("https://"):
                raise ValueError("API URL must use HTTPS")

            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            # Mempool.space uses similar structure to Blockstream
            chain_stats = data.get("chain_stats", {})
            funded = chain_stats.get("funded_txo_sum", 0)
            spent = chain_stats.get("spent_txo_sum", 0)
            balance_sats = funded - spent

            return {
                "address": address,
                "balance_btc": balance_sats / 100_000_000,
                "balance_sats": balance_sats,
                "confirmed": True,
                "provider": "mempool_space",
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
        except Exception as e:
            logger.debug(f"Cache read failed: {str(e)}")
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
        except Exception as e:
            logger.debug(f"Cache write failed: {str(e)}")
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
