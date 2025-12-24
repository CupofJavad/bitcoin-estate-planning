# Code Adoption Guidelines - Learning from Open Source

## Philosophy
**"Stand on the shoulders of giants, but understand what you're standing on."**

We learn from existing implementations but adapt them to our architecture and security requirements.

## Adoption Process

### Step 1: Research & Identify
1. Identify the pattern/functionality needed
2. Find reputable repositories with similar implementations
3. Review their approach and rationale
4. Document why their approach is good

### Step 2: Security Review
1. **License Check**: Ensure compatible license
2. **Code Review**: Look for:
   - Hardcoded secrets
   - Backdoors or suspicious code
   - Security vulnerabilities
   - Dependency vulnerabilities
3. **Community Review**: Check if code has been reviewed by community
4. **Maintenance Status**: Ensure code is actively maintained

### Step 3: Understand & Adapt
1. **Understand the Code**: Don't copy without understanding
2. **Adapt to Our Architecture**: Fit into our patterns
3. **Add Our Tests**: Write comprehensive tests
4. **Document Source**: Credit the inspiration

### Step 4: Implementation
1. Implement in our style
2. Add security enhancements
3. Integrate with our error handling
4. Add logging and monitoring

## Specific Patterns to Research

### From eigenwallet/core

#### 1. Multi-Source Data Validation
**Pattern**: Use multiple sources and validate consistency
```python
# Inspired by eigenwallet's multi-exchange approach
async def get_balance_multi_source(address):
    sources = [
        get_blockstream_balance,
        get_blockchain_info_balance,
        get_mempool_balance,
    ]
    
    results = await asyncio.gather(*[s(address) for s in sources], return_exceptions=True)
    valid_results = [r for r in results if not isinstance(r, Exception)]
    
    if len(valid_results) < 2:
        raise Exception("Insufficient data sources")
    
    # Validate consistency (10% threshold)
    avg = sum(valid_results) / len(valid_results)
    for result in valid_results:
        if abs(result - avg) / avg > 0.10:
            raise Exception("Data inconsistency detected")
    
    return avg
```

#### 2. Connection Resilience
**Pattern**: Exponential backoff with retry
```python
# Inspired by eigenwallet's P2P reconnection logic
async def resilient_request(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            await asyncio.sleep(wait_time)
```

#### 3. Background Processing
**Pattern**: Validate/process in background
```python
# Inspired by eigenwallet's background wallet scanning
async def validate_address_background(address: str):
    """Validate address in background, update UI when done."""
    # Immediate format check
    format_valid = check_format(address)
    
    # Background checksum validation
    asyncio.create_task(validate_checksum_async(address))
    
    return format_valid
```

## Security Checklist for Adopted Code

### Before Adoption
- [ ] License is compatible
- [ ] Code has been security reviewed
- [ ] No hardcoded secrets
- [ ] No suspicious network calls
- [ ] Dependencies are secure
- [ ] Code is actively maintained

### During Adaptation
- [ ] Remove any hardcoded values
- [ ] Add our error handling
- [ ] Integrate with our logging
- [ ] Add security logging
- [ ] Add input validation
- [ ] Add rate limiting

### After Implementation
- [ ] Code review by team
- [ ] Security testing
- [ ] Performance testing
- [ ] Documentation updated
- [ ] Source credited

## Example: Adopting Address Validation

### Original (from Bitcoin Core concepts)
```python
# Simplified version of Bitcoin Core validation
def validate_address_core_style(address):
    # Format check
    if not address.startswith(('1', '3', 'bc1', 'tb1')):
        return False
    
    # Length check
    if len(address) < 26 or len(address) > 74:
        return False
    
    # Checksum validation
    return validate_checksum(address)
```

### Our Adapted Version
```python
# Adapted to our architecture
class BitcoinAddressValidator:
    """Validates Bitcoin addresses with comprehensive checks."""
    
    def validate(self, address: str) -> Dict[str, any]:
        """Validate with detailed error reporting."""
        errors = []
        
        # Format check
        format_result = self._check_format(address)
        if not format_result["valid"]:
            errors.extend(format_result["errors"])
        
        # Checksum validation
        if not self._validate_checksum(address):
            errors.append("Checksum validation failed")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "format": format_result.get("format"),
        }
```

**Key Differences:**
- ✅ Better error reporting
- ✅ Structured return value
- ✅ Integration with our patterns
- ✅ Comprehensive validation

## Documentation Requirements

When adopting code, document:

1. **Source**: Where did the pattern come from?
2. **Rationale**: Why did we adopt it?
3. **Adaptations**: What did we change and why?
4. **Security**: What security considerations were made?
5. **Tests**: What tests were added?

Example:
```python
"""
Bitcoin address validation.

Pattern inspired by Bitcoin Core's validation approach, adapted for our
service architecture with enhanced error reporting.

Source: Bitcoin Core validation concepts
Adaptations:
  - Added structured error reporting
  - Integrated with our validation service pattern
  - Added network-specific validation

Security:
  - Validates locally before external API calls
  - Checksum validation prevents typos
  - No external dependencies for validation
"""
```

## Conclusion

**Adopting code from reputable repositories is valuable when:**
- ✅ We understand the code
- ✅ We adapt it to our needs
- ✅ We review it for security
- ✅ We add our own tests
- ✅ We document the source

**We should avoid:**
- ❌ Blind copy-pasting
- ❌ Adopting without understanding
- ❌ Ignoring security reviews
- ❌ Not adapting to our architecture
- ❌ Not crediting sources

