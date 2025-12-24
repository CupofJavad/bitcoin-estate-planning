"""Bitcoin-related API endpoints."""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.services.bitcoin_validator import validate_bitcoin_address, BitcoinAddressValidator
from app.services.bitcoin_balance import get_bitcoin_balance
from app.core.config import settings

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
    network = request.network or settings.BITCOIN_NETWORK
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
    """Get Bitcoin balance for an address.

    **Security Notes:**
    - Address is validated before any external API calls
    - All API calls use HTTPS only
    - Results are cached to reduce API load
    - Rate limiting should be implemented at the application level

    **Rate Limits:**
    - Blockstream API: ~1 request/second
    - Cached results: 5 minutes TTL
    """
    # Validate address first (security requirement)
    validation = validate_bitcoin_address(address, network=settings.BITCOIN_NETWORK)
    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Bitcoin address: {', '.join(validation.get('errors', []))}",
        )

    # Get balance
    balance_data = await get_bitcoin_balance(
        address, network=settings.BITCOIN_NETWORK, use_cache=use_cache
    )

    if balance_data.get("error"):
        raise HTTPException(
            status_code=503, detail=balance_data["error"]
        )

    return balance_data

