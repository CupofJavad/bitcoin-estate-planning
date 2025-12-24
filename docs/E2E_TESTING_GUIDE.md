# E2E Testing Guide

## Overview

This project includes comprehensive end-to-end (E2E) testing using Playwright, covering all user workflows, interactions, and error scenarios.

## Test Infrastructure

### Components

1. **Playwright** - Browser automation framework
2. **Error Logger** - Advanced error logging system (frontend + backend)
3. **Test Suites** - Comprehensive coverage of all workflows

### Test Coverage

- ✅ **Authentication**: Registration, login, logout, error handling
- ✅ **Estate Plans**: Create, read, update, delete operations
- ✅ **Beneficiaries**: Create, validate allocation percentages
- ✅ **Navigation**: Menus, buttons, links, theme toggle
- ✅ **Error Handling**: Network errors, validation errors, API errors

## Running Tests

### Prerequisites

1. **Backend running**: `http://localhost:8000`
2. **Frontend running**: `http://localhost:3004` (or 3000)
3. **Playwright installed**: Browsers will be installed automatically

### Quick Start

```bash
# Using the test runner script (recommended)
./scripts/run-e2e-tests.sh

# Or manually
cd frontend/client-portal
npm run test:e2e
```

### Test Commands

```bash
# Run all tests
npm run test:e2e

# Run with UI (interactive)
npm run test:e2e:ui

# Run in debug mode
npm run test:e2e:debug

# View test report
npm run test:e2e:report
```

## Test Files

### `tests/e2e/auth.spec.ts`
- User registration
- Login with valid/invalid credentials
- Logout
- Form validation
- Navigation between login/register

### `tests/e2e/estate-plans.spec.ts`
- Create estate plan
- View estate plan details
- Edit estate plan
- Delete estate plan
- Dashboard display

### `tests/e2e/beneficiaries.spec.ts`
- Create beneficiary
- Validate allocation percentages
- Form validation

### `tests/e2e/navigation.spec.ts`
- Dashboard navigation
- Detail page navigation
- Theme toggle
- User menu
- Browser back/forward

## Error Logging

### Frontend Error Logger

Located in `lib/error-logger.ts`, captures:
- Error messages and stack traces
- Request/response details
- User context (URL, user agent, user ID)
- Component and action information

### Backend Error Logging Endpoint

`POST /api/v1/logs/error` - Receives error logs from frontend

### Viewing Error Logs

1. **Browser Console**: Check DevTools console for error logs
2. **Backend Logs**: Check backend terminal output
3. **Test Reports**: Playwright HTML report includes console logs

## Analyzing Test Results

### Test Report

After running tests, view the HTML report:

```bash
npm run test:e2e:report
```

The report includes:
- Test results (passed/failed)
- Screenshots of failures
- Video recordings (on failure)
- Console logs
- Network requests

### Common Issues and Fixes

#### 1. "Unexpected end of JSON input" (NextAuth)

**Symptom**: Error in browser console when loading session

**Fix**: 
- Check `NEXTAUTH_SECRET` is set in `.env.local`
- Verify backend is running and accessible
- Check CORS configuration includes frontend URL

#### 2. Tests Timeout

**Symptom**: Tests fail with timeout errors

**Fix**:
- Ensure backend is running: `curl http://localhost:8000/health`
- Ensure frontend is running: `curl http://localhost:3004`
- Increase timeout in test: `await page.waitForSelector(selector, { timeout: 10000 })`

#### 3. Element Not Found

**Symptom**: `Element not found` errors

**Fix**:
- Check if element selector is correct
- Verify element is visible (not hidden by CSS)
- Add wait for element: `await page.waitForSelector(selector)`

#### 4. Authentication Failures

**Symptom**: Tests fail at login/registration

**Fix**:
- Check backend API is responding: `curl http://localhost:8000/api/v1/auth/register`
- Verify test user credentials
- Check error logs in browser console

## Debugging Failed Tests

### Step 1: Run in Debug Mode

```bash
npm run test:e2e:debug
```

This opens Playwright Inspector where you can:
- Step through test execution
- Inspect page state
- View console logs
- Check network requests

### Step 2: Check Error Logs

1. **Browser Console**: Open DevTools during test execution
2. **Backend Logs**: Check terminal running backend
3. **Test Report**: View detailed error information

### Step 3: Analyze Network Requests

In Playwright Inspector or test report:
- Check failed API requests
- Verify request headers
- Check response status codes
- Review response bodies

### Step 4: Research Solutions

For each error:
1. Extract error message and stack trace
2. Search for similar issues online
3. Check project documentation
4. Review recent code changes

### Step 5: Apply Fixes

1. Fix the issue in code
2. Add/update tests if needed
3. Re-run tests to verify fix
4. Document the fix

## Continuous Testing

### Running Tests in CI/CD

Add to your CI pipeline:

```yaml
# Example GitHub Actions
- name: Install dependencies
  run: |
    cd frontend/client-portal
    npm install
    npx playwright install --with-deps

- name: Run E2E tests
  run: |
    cd frontend/client-portal
    npm run test:e2e
  env:
    FRONTEND_URL: http://localhost:3000
    API_URL: http://localhost:8000
```

## Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Clean State**: Clear cookies/storage before each test
3. **Wait for Elements**: Always wait for elements before interacting
4. **Use Data Attributes**: Prefer `data-testid` for selectors
5. **Handle Async**: Properly await async operations
6. **Error Handling**: Test both success and error scenarios
7. **Documentation**: Document complex test scenarios

## Adding New Tests

### Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: login, navigate, etc.
  });

  test('should perform action', async ({ page }) => {
    // Arrange
    await page.goto('/path');
    
    // Act
    await page.click('button');
    
    // Assert
    await expect(page.locator('element')).toBeVisible();
  });
});
```

### Guidelines

1. **Descriptive Names**: Test names should clearly describe what they test
2. **One Assertion**: Each test should verify one behavior
3. **Setup/Cleanup**: Use `beforeEach`/`afterEach` for common setup
4. **Error Logging**: Use error logger for debugging
5. **Screenshots**: Playwright automatically captures screenshots on failure

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Next.js Testing Guide](https://nextjs.org/docs/app/building-your-application/testing)
- [Error Logging Documentation](./ERROR_LOGGING.md)

---

**Last Updated**: December 2024

