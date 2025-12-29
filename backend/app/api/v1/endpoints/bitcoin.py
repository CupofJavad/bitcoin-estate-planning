"""Bitcoin-related API endpoints.

Enhanced with multi-API fallback, deviation validation, and robust error handling.
Patterns inspired by eigenwallet/core, Bitcoin Core, and BTCPay Server.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import logging

from app.services.bitcoin_validator import validate_bitcoin_address, BitcoinAddressValidator
from app.services.bitcoin_balance import get_bitcoin_balance
from app.core.config import settings
from app.utils.error_handling import handle_bitcoin_error, ErrorCategory

logger = logging.getLogger(__name__)

router = APIRouter()


class AddressValidationRequest(BaseModel):
    """Request model for address validation."""
    address: str
    network: Optional[str] = None


class AddressValidationResponse(BaseModel):
    """Response model for address validation."""
    valid: bool
    format: str
    network: str
    errors: list[str]


@router.post("/validate", response_model=AddressValidationResponse)
async def validate_address(request: AddressValidationRequest):
    """Validate a Bitcoin address.

    Validates the address format and checksum before any external API calls.
    This is a security best practice - always validate locally first.
    """
    # Auto-detect network from address if not explicitly provided.
    # This allows using both mainnet and testnet addresses in the UI.
    network = request.network
    if not network:
        addr = request.address.strip()
        if addr.startswith("bc1") or addr.startswith(("1", "3")):
            network = "mainnet"
        elif addr.startswith("tb1"):
            network = "testnet"
        else:
            network = settings.BITCOIN_NETWORK

    result = validate_bitcoin_address(request.address, network=network)

    return AddressValidationResponse(
        valid=result["valid"],
        format=result["format"],
        network=result["network"],
        errors=result.get("errors", []),
    )


@router.get("/balance/{address}")
async def get_balance(
    address: str,
    use_cache: bool = Query(True, description="Use cached balance if available"),
):
    """Get Bitcoin balance for an address with multi-API fallback.

    **Features:**
    - Multi-API fallback (Blockstream, Blockchain.info, Mempool.space)
    - Deviation threshold validation (10% consistency check)
    - Exponential backoff retry logic
    - Comprehensive error handling

    **Security Notes:**
    - Address is validated before any external API calls
    - All API calls use HTTPS only
    - Results are cached to reduce API load
    - Rate limiting should be implemented at the application level

    **Rate Limits:**
    - Blockstream API: ~1 request/second
    - Cached results: 5 minutes TTL

    **Patterns:**
    - Multi-API fallback inspired by eigenwallet/core
    - Error handling inspired by Bitcoin Core and BTCPay Server
    """
    try:
        # Validate address first (security requirement)
        validation = validate_bitcoin_address(address, network=settings.BITCOIN_NETWORK)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid Bitcoin address: {', '.join(validation.get('errors', []))}",
            )

        # Get balance with multi-API fallback
        balance_data = await get_bitcoin_balance(
            address, network=settings.BITCOIN_NETWORK, use_cache=use_cache
        )

        if balance_data.get("error"):
            # Use enhanced error handling
            bitcoin_error = handle_bitcoin_error(
                Exception(balance_data["error"]), context="balance_check"
            )
            raise HTTPException(
                status_code=503,
                detail=bitcoin_error.user_message,
            )

        return balance_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in balance endpoint: {str(e)}")
        bitcoin_error = handle_bitcoin_error(e, context="balance_endpoint")
        raise HTTPException(
            status_code=500,
            detail=bitcoin_error.user_message,
        )

