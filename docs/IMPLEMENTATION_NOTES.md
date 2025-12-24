# Implementation Notes - Adopted Patterns

## Overview
This document tracks patterns and approaches adopted from other Bitcoin projects.

## Patterns Implemented

### 1. Multi-API Fallback (from eigenwallet/core)

**Source**: eigenwallet/core uses multiple exchanges (Kraken, Bitfinex, KuCoin) for price data

**Implementation**: `backend/app/services/bitcoin_balance.py`

**Features**:
- Multiple API providers with priority ordering
- Automatic fallback if primary API fails
- Provider abstraction for easy addition of new APIs

**Providers**:
1. Blockstream (priority 1) - Primary
2. Blockchain.info (priority 2) - Fallback
3. Mempool.space (priority 3) - Secondary fallback

**Code Pattern**:
```python
# Try providers in priority order
for provider in sorted_providers:
    try:
        result = await fetch_from_provider(provider, address)
        if result:
            return result
    except Exception:
        continue  # Try next provider
```

### 2. Deviation Threshold Validation (from eigenwallet/core)

**Source**: eigenwallet rejects data if deviation >10% from average

**Implementation**: `BitcoinBalanceService._validate_balance_consistency()`

**Features**:
- Validates consistency across multiple API results
- 10% deviation threshold (configurable)
- Logs inconsistencies for monitoring
- Uses highest priority result if inconsistency detected

**Code Pattern**:
```python
def validate_balance_consistency(results):
    avg = sum(balances) / len(balances)
    for balance in balances:
        deviation = abs(balance - avg) / avg
        if deviation > 0.10:  # 10% threshold
            return False
    return True
```

### 3. Exponential Backoff Retry (from eigenwallet/core)

**Source**: eigenwallet's P2P connection resilience patterns

**Implementation**: `BitcoinBalanceService._fetch_from_provider()`

**Features**:
- Exponential backoff: 1s, 2s, 4s delays
- Maximum 3 retries per provider
- Logs retry attempts for debugging

**Code Pattern**:
```python
for attempt in range(MAX_RETRIES):
    try:
        return await fetch_data()
    except Exception:
        if attempt == MAX_RETRIES - 1:
            raise
        wait_time = INITIAL_DELAY * (2 ** attempt)
        await asyncio.sleep(wait_time)
```

### 4. Enhanced Error Handling (from Bitcoin Core, BTCPay Server)

**Source**: Bitcoin Core's comprehensive error classification

**Implementation**: `backend/app/utils/error_handling.py`

**Features**:
- Error categorization (validation, network, API, security, etc.)
- User-friendly error messages
- Detailed logging for debugging
- Security event logging

**Error Categories**:
- `VALIDATION`: Invalid input
- `NETWORK`: Connection issues
- `API`: External API errors
- `SECURITY`: Security-related errors
- `RATE_LIMIT`: Rate limiting
- `CACHE`: Caching errors
- `UNKNOWN`: Unclassified errors

### 5. Address Validation (from Bitcoin Core concepts)

**Source**: Bitcoin Core's validation algorithms

**Implementation**: `backend/app/services/bitcoin_validator.py`

**Features**:
- Multi-format support (P2PKH, P2SH, Bech32)
- Checksum validation (Base58 and Bech32)
- Network validation (mainnet/testnet)
- Comprehensive error reporting

## Security Enhancements

### 1. HTTPS Enforcement
- All external API calls must use HTTPS
- Validates URL scheme before making requests
- Raises error if non-HTTPS URL detected

### 2. Input Validation First
- Addresses validated locally before any external calls
- Prevents invalid addresses from reaching APIs
- Reduces API abuse

### 3. Error Message Sanitization
- Generic error messages for users
- Detailed errors only in logs
- No sensitive information in responses

### 4. Security Event Logging
- Logs security-relevant events
- Partial address logging (privacy)
- Event classification

## Performance Optimizations

### 1. Redis Caching
- 5-minute TTL for balance results
- Reduces external API calls
- Improves response times

### 2. Parallel API Calls
- Can fetch from multiple APIs concurrently
- Faster fallback when primary fails
- Better user experience

### 3. Provider Priority
- Highest priority provider tried first
- Faster responses for common cases
- Fallback only when needed

## Testing Considerations

### Unit Tests Needed
- [ ] Multi-API fallback logic
- [ ] Deviation threshold validation
- [ ] Exponential backoff retry
- [ ] Error handling and classification
- [ ] Cache behavior

### Integration Tests Needed
- [ ] End-to-end balance checking
- [ ] API failure scenarios
- [ ] Network timeout handling
- [ ] Cache hit/miss scenarios

## Future Enhancements

### 1. Rate Limiting
- Per-IP rate limiting
- Per-user rate limiting (when auth is added)
- Distributed rate limiting (Redis-based)

### 2. API Health Monitoring
- Track API provider availability
- Automatic provider priority adjustment
- Health check endpoints

### 3. Advanced Caching
- Cache warming
- Cache invalidation strategies
- Cache statistics

### 4. Self-Hosted Node Option
- Direct Bitcoin Core RPC integration
- Most secure option
- No external API dependencies

## References

- [eigenwallet/core](https://github.com/eigenwallet/core) - Multi-source validation patterns
- [Bitcoin Core](https://github.com/bitcoin/bitcoin) - Validation algorithms
- [BTCPay Server](https://github.com/btcpayserver/btcpayserver) - Production patterns
- [Blockstream API](https://blockstream.info/api/) - API design

