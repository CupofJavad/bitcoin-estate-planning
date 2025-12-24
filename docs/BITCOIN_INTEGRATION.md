# Bitcoin Integration - Address Validation & Balance Checking

## Overview
This document outlines the secure implementation of Bitcoin address validation and wallet balance checking for the Bitcoin Estate Planning Platform.

## Security Considerations

### Critical Security Requirements
1. **Local Validation First**: Always validate addresses locally before any external API calls
2. **HTTPS Only**: All external API calls must use HTTPS/TLS encryption
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Caching**: Cache balance results to reduce API calls and improve performance
5. **Error Handling**: Never expose sensitive information in error messages
6. **Input Sanitization**: Validate and sanitize all user inputs
7. **Audit Logging**: Log all validation and balance check attempts

### Threat Model
- **Address Tampering**: Users might input invalid addresses to test system
- **API Abuse**: Malicious users might spam balance check endpoints
- **Man-in-the-Middle**: Unencrypted connections could be intercepted
- **Data Leakage**: Error messages might reveal system internals

## Bitcoin Address Validation

### Address Formats
Bitcoin addresses come in three main formats:

1. **P2PKH (Legacy)**: Starts with `1`, Base58 encoded
   - Example: `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
   - Length: 26-35 characters
   - Contains checksum (like Luhn algorithm for credit cards)

2. **P2SH (Script Hash)**: Starts with `3`, Base58 encoded
   - Example: `3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy`
   - Length: 26-35 characters
   - Contains checksum

3. **Bech32 (Native SegWit)**: Starts with `bc1` (mainnet) or `tb1` (testnet)
   - Example: `bc1qzwuucm74lmhrg2guvlr2dntk2g2gxu5e84taq8`
   - Length: 14-74 characters (typically 42-62)
   - Built-in error detection (Bech32 checksum)

### Validation Rules
1. **Format Check**: Verify address matches one of the three formats
2. **Length Check**: Verify address length is within valid range
3. **Character Set Check**: Verify only valid characters are used
4. **Checksum Validation**: Verify checksum is correct (prevents typos)
5. **Network Check**: Verify address matches configured network (mainnet/testnet)

### Implementation Strategy
- Use established libraries (`base58`, `bech32`) for validation
- Validate locally (no external API needed for format validation)
- Provide immediate feedback to users
- Show helpful error messages for common mistakes

## Balance Checking

### API Options

#### Option 1: Blockstream API (Recommended)
- **URL**: `https://blockstream.info/api/` (mainnet) or `https://blockstream.info/testnet/api/` (testnet)
- **Free**: Yes, with rate limits
- **Trust**: High (widely used, open source)
- **Rate Limits**: ~1 request/second (should be sufficient with caching)
- **Security**: HTTPS only, no API key required for basic queries

**Endpoint**: `GET /address/{address}`

**Response**:
```json
{
  "address": "bc1q...",
  "chain_stats": {
    "funded_txo_count": 1,
    "funded_txo_sum": 100000000,
    "spent_txo_count": 0,
    "spent_txo_sum": 0,
    "tx_count": 1
  },
  "mempool_stats": {...}
}
```

#### Option 2: Blockchain.info API
- **URL**: `https://blockchain.info/q/addressbalance/{address}`
- **Free**: Yes, with rate limits
- **Trust**: High (established service)
- **Rate Limits**: ~1 request/second
- **Security**: HTTPS only

#### Option 3: Self-Hosted Bitcoin Node
- **Pros**: Full control, no rate limits, most secure
- **Cons**: Requires running Bitcoin Core, high resource usage
- **Use Case**: Production environments with high security requirements

### Implementation Strategy
1. **Validate Address First**: Never check balance of invalid addresses
2. **Cache Results**: Cache balance for 5-10 minutes to reduce API calls
3. **Rate Limiting**: Limit balance checks per user/IP
4. **Async Processing**: Make balance checks non-blocking
5. **Error Handling**: Handle API failures gracefully
6. **Fallback**: Consider multiple API providers for redundancy

### Security Best Practices
1. **HTTPS Only**: All external API calls must use HTTPS
2. **Timeout**: Set reasonable timeouts (5-10 seconds)
3. **Retry Logic**: Implement exponential backoff for retries
4. **Rate Limiting**: Prevent abuse with rate limiting
5. **Caching**: Reduce external API calls with Redis caching
6. **Logging**: Log all balance check attempts (without sensitive data)

## Implementation Plan

### Phase 1: Address Validation (Priority: High)
- [x] Research Bitcoin address formats and validation
- [ ] Install validation libraries (`base58`, `bech32`)
- [ ] Create `BitcoinAddressValidator` service
- [ ] Add validation to Estate Plan and Beneficiary forms
- [ ] Add real-time validation feedback in UI
- [ ] Write tests for validation logic

### Phase 2: Balance Checking (Priority: Medium)
- [ ] Design balance checking service architecture
- [ ] Implement Blockstream API client
- [ ] Add Redis caching for balance results
- [ ] Implement rate limiting
- [ ] Add balance display to UI (optional, for demo)
- [ ] Write tests for balance checking

### Phase 3: Security Hardening (Priority: High)
- [ ] Review all external API calls for HTTPS
- [ ] Implement comprehensive error handling
- [ ] Add audit logging
- [ ] Review and update security documentation
- [ ] Security audit and penetration testing

## Code Structure

```
backend/app/
├── services/
│   ├── __init__.py
│   ├── bitcoin_validator.py      # Address validation
│   └── bitcoin_balance.py        # Balance checking
├── utils/
│   └── security.py               # Security utilities
```

## Dependencies

### Python Libraries
- `base58>=2.1.0` - Base58 encoding/decoding
- `bech32>=1.2.0` - Bech32 encoding/decoding
- `httpx>=0.27.0` - Async HTTP client (already included)
- `redis>=5.0.0` - Caching (already included)

## API Endpoints

### Validate Address
```
POST /api/v1/bitcoin/validate
{
  "address": "bc1q...",
  "network": "testnet"  // optional, defaults to config
}

Response:
{
  "valid": true,
  "format": "bech32",
  "network": "testnet",
  "errors": []
}
```

### Check Balance (Optional)
```
GET /api/v1/bitcoin/balance/{address}

Response:
{
  "address": "bc1q...",
  "balance_btc": 0.001,
  "balance_sats": 100000,
  "confirmed": true,
  "cached": false,
  "last_updated": "2025-12-24T10:00:00Z"
}
```

## Testing Strategy

1. **Unit Tests**: Test validation logic with various address formats
2. **Integration Tests**: Test API calls to Blockstream (with mocking)
3. **Security Tests**: Test rate limiting, input sanitization
4. **Performance Tests**: Test caching effectiveness

## Future Enhancements

1. **Multi-API Fallback**: Support multiple balance check APIs
2. **WebSocket Updates**: Real-time balance updates
3. **Transaction History**: Show recent transactions
4. **Address Monitoring**: Monitor addresses for changes
5. **Self-Hosted Node**: Option to use local Bitcoin node

