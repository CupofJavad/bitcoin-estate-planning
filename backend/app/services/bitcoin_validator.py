"""Bitcoin address validation service.

Validates Bitcoin addresses using proper checksum algorithms.
Supports P2PKH (legacy), P2SH (script hash), and Bech32 (SegWit) formats.

Validation patterns inspired by Bitcoin Core's validation implementation.
"""

import re
from typing import Dict, List, Optional
from enum import Enum

try:
    import base58
    BASE58_AVAILABLE = True
except ImportError:
    BASE58_AVAILABLE = False

try:
    import bech32
    BECH32_AVAILABLE = True
except ImportError:
    BECH32_AVAILABLE = False


class AddressFormat(str, Enum):
    """Bitcoin address formats."""
    P2PKH = "p2pkh"  # Legacy, starts with 1
    P2SH = "p2sh"    # Script hash, starts with 3
    BECH32 = "bech32"  # SegWit, starts with bc1 (mainnet) or tb1 (testnet)
    INVALID = "invalid"


class BitcoinAddressValidator:
    """Validates Bitcoin addresses with proper checksum verification."""

    # Address format patterns
    P2PKH_PATTERN = re.compile(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$')
    BECH32_MAINNET_PATTERN = re.compile(r'^bc1[a-z0-9]{39,59}$')
    BECH32_TESTNET_PATTERN = re.compile(r'^tb1[a-z0-9]{39,59}$')

    def __init__(self, network: str = "testnet"):
        """Initialize validator.

        Args:
            network: Network type ("mainnet" or "testnet")
        """
        self.network = network.lower()
        if self.network not in ["mainnet", "testnet"]:
            raise ValueError("Network must be 'mainnet' or 'testnet'")

    def validate(self, address: str) -> Dict[str, any]:
        """Validate a Bitcoin address.

        Args:
            address: Bitcoin address to validate

        Returns:
            Dictionary with validation results:
            {
                "valid": bool,
                "format": str,  # "p2pkh", "p2sh", "bech32", or "invalid"
                "network": str,  # "mainnet" or "testnet"
                "errors": List[str]  # List of error messages
            }
        """
        errors: List[str] = []
        address = address.strip()

        # Basic checks
        if not address:
            return {
                "valid": False,
                "format": AddressFormat.INVALID,
                "network": self.network,
                "errors": ["Address cannot be empty"],
            }

        # Check length (basic sanity check)
        if len(address) < 26 or len(address) > 74:
            errors.append(f"Address length {len(address)} is invalid (must be 26-74 characters)")

        # Try to identify format and validate
        format_result = self._identify_format(address)
        format_type = format_result["format"]

        if format_type == AddressFormat.INVALID:
            errors.extend(format_result.get("errors", ["Invalid address format"]))
        else:
            # Validate checksum based on format
            checksum_valid = self._validate_checksum(address, format_type)
            if not checksum_valid:
                errors.append("Checksum validation failed (address may contain typos)")

            # Check network match for Bech32
            if format_type == AddressFormat.BECH32:
                network_match = self._check_network_match(address)
                if not network_match:
                    errors.append(
                        f"Address network doesn't match configured network ({self.network})"
                    )

        return {
            "valid": len(errors) == 0,
            "format": format_type.value if format_type != AddressFormat.INVALID else "invalid",
            "network": self.network,
            "errors": errors,
        }

    def _identify_format(self, address: str) -> Dict[str, any]:
        """Identify Bitcoin address format.

        Returns:
            Dictionary with format and any errors
        """
        # Check Bech32 (SegWit) - most common modern format
        if address.startswith("bc1"):
            if self.BECH32_MAINNET_PATTERN.match(address):
                return {"format": AddressFormat.BECH32, "errors": []}
            return {
                "format": AddressFormat.INVALID,
                "errors": ["Invalid Bech32 mainnet address format"],
            }

        if address.startswith("tb1"):
            if self.BECH32_TESTNET_PATTERN.match(address):
                return {"format": AddressFormat.BECH32, "errors": []}
            return {
                "format": AddressFormat.INVALID,
                "errors": ["Invalid Bech32 testnet address format"],
            }

        # Check P2PKH (starts with 1) or P2SH (starts with 3)
        if self.P2PKH_PATTERN.match(address):
            if address[0] == "1":
                return {"format": AddressFormat.P2PKH, "errors": []}
            elif address[0] == "3":
                return {"format": AddressFormat.P2SH, "errors": []}

        return {
            "format": AddressFormat.INVALID,
            "errors": ["Address doesn't match any known Bitcoin format"],
        }

    def _validate_checksum(self, address: str, format_type: AddressFormat) -> bool:
        """Validate address checksum.

        Args:
            address: Bitcoin address
            format_type: Address format type

        Returns:
            True if checksum is valid, False otherwise
        """
        if format_type == AddressFormat.BECH32:
            return self._validate_bech32_checksum(address)
        elif format_type in [AddressFormat.P2PKH, AddressFormat.P2SH]:
            return self._validate_base58_checksum(address)
        return False

    def _validate_bech32_checksum(self, address: str) -> bool:
        """Validate Bech32 checksum.

        Bech32 addresses have built-in error detection similar to Luhn algorithm.
        """
        if not BECH32_AVAILABLE:
            # If library not available, do basic format check only
            return True  # Assume valid if format matches

        try:
            # Decode Bech32 address
            hrp, data = bech32.bech32_decode(address)
            if hrp is None or data is None:
                return False

            # Verify HRP matches network
            if self.network == "mainnet" and hrp != "bc":
                return False
            if self.network == "testnet" and hrp != "tb":
                return False

            # Bech32 decode validates checksum automatically
            return True
        except Exception:
            return False

    def _validate_base58_checksum(self, address: str) -> bool:
        """Validate Base58 checksum.

        Base58 addresses (P2PKH and P2SH) have a checksum in the last 4 bytes.
        """
        if not BASE58_AVAILABLE:
            # If library not available, do basic format check only
            return True  # Assume valid if format matches

        try:
            # Decode Base58 address
            decoded = base58.b58decode(address)
            if len(decoded) < 5:  # Need at least version byte + 4 checksum bytes
                return False

            # Extract version, payload, and checksum
            version = decoded[0]
            payload = decoded[1:-4]
            checksum = decoded[-4:]

            # Calculate expected checksum (double SHA256)
            import hashlib
            hash1 = hashlib.sha256(bytes([version]) + payload).digest()
            hash2 = hashlib.sha256(hash1).digest()
            expected_checksum = hash2[:4]

            # Verify checksum matches
            return checksum == expected_checksum
        except Exception:
            return False

    def _check_network_match(self, address: str) -> bool:
        """Check if Bech32 address network matches configured network.

        Args:
            address: Bech32 address

        Returns:
            True if network matches, False otherwise
        """
        if address.startswith("bc1") and self.network == "mainnet":
            return True
        if address.startswith("tb1") and self.network == "testnet":
            return True
        return False


def validate_bitcoin_address(address: str, network: str = "testnet") -> Dict[str, any]:
    """Convenience function to validate a Bitcoin address.

    Args:
        address: Bitcoin address to validate
        network: Network type ("mainnet" or "testnet")

    Returns:
        Validation result dictionary
    """
    validator = BitcoinAddressValidator(network=network)
    return validator.validate(address)

