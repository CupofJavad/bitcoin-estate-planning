# Comprehensive Testing Guide

## Overview

This guide covers all testing strategies for the Bitcoin Estate Planning Platform, including unit tests, integration tests, E2E tests, load testing, and security audits.

## Test Structure

```
backend/
  tests/
    test_api_integration.py      # Integration tests
    test_services.py              # Service unit tests
    test_models.py                # Model tests

frontend/client-portal/
  tests/
    e2e/
      auth.spec.ts               # Authentication E2E tests
      estate-plans.spec.ts        # Estate plans E2E tests
      beneficiaries.spec.ts       # Beneficiaries E2E tests
      navigation.spec.ts          # Navigation E2E tests
    helpers/
      auth.ts                     # Auth test helpers
```

## Running Tests

### Backend Tests

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

### Frontend E2E Tests

```bash
cd frontend/client-portal
npm run test:e2e
```

### All Tests

```bash
# Backend
cd backend && pytest tests/ -v

# Frontend
cd frontend/client-portal && npm run test:e2e
```

## Test Types

### 1. Unit Tests

**Purpose**: Test individual functions and methods in isolation.

**Location**: `backend/tests/test_*.py`

**Example**:
```python
def test_bitcoin_address_validation():
    result = validate_bitcoin_address("tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx")
    assert result["valid"] == True
```

### 2. Integration Tests

**Purpose**: Test API endpoints and database interactions.

**Location**: `backend/tests/test_api_integration.py`

**Example**:
```python
async def test_create_estate_plan(client, auth_headers):
    response = await client.post(
        "/api/v1/estate-plans",
        json={"name": "Test Plan"},
        headers=auth_headers
    )
    assert response.status_code == 200
```

### 3. E2E Tests

**Purpose**: Test complete user workflows in the browser.

**Location**: `frontend/client-portal/tests/e2e/*.spec.ts`

**Example**:
```typescript
test('should create estate plan', async ({ page }) => {
  await loginUser(page, testUser)
  await page.goto('/')
  await page.click('text=Create Estate Plan')
  // ... fill form and submit
})
```

## Test Coverage Goals

- **Backend**: 80%+ code coverage
- **Frontend**: Critical paths covered by E2E tests
- **API Endpoints**: 100% endpoint coverage

## Load Testing

### Using Locust

```bash
pip install locust
locust -f tests/load_test.py
```

### Key Metrics

- **Response Time**: < 500ms for 95th percentile
- **Throughput**: 100+ requests/second
- **Error Rate**: < 1%

## Security Testing

### Checklist

- [ ] SQL Injection prevention
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Authentication bypass attempts
- [ ] Authorization checks
- [ ] Input validation
- [ ] Rate limiting
- [ ] Secrets management

### Tools

- OWASP ZAP for security scanning
- Bandit for Python security linting
- ESLint security plugins for frontend

## Continuous Integration

Tests run automatically on:
- Pull requests to `main` or `develop`
- Pushes to `main` branch

See `.github/workflows/ci.yml` for configuration.

## Test Data

- Use test fixtures for consistent test data
- Clean up test data after tests
- Use separate test database

## Best Practices

1. **Isolation**: Each test should be independent
2. **Speed**: Tests should run quickly (< 1 minute total)
3. **Clarity**: Test names should describe what they test
4. **Coverage**: Test both happy paths and error cases
5. **Maintenance**: Keep tests updated with code changes

## Troubleshooting

### Tests Fail Locally But Pass in CI

- Check environment variables
- Verify database state
- Check for race conditions

### E2E Tests Timeout

- Increase timeout values
- Check if services are running
- Verify network connectivity

### Flaky Tests

- Add proper waits
- Use stable selectors
- Avoid timing-dependent assertions

