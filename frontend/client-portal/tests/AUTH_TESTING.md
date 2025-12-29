# Authentication Testing Guide

## Overview

This document describes the authentication testing strategy and test coverage for the Bitcoin Estate Planning Platform.

## Test Coverage

### E2E Tests (`tests/e2e/auth.spec.ts`)

The authentication E2E tests cover:

1. **Registration Flow**
   - ✅ Display registration page
   - ✅ Register new user successfully
   - ✅ Show error for invalid email format
   - ✅ Show error for short password
   - ✅ Navigate between login and register pages

2. **Login Flow**
   - ✅ Display login page
   - ✅ Login with valid credentials
   - ✅ Show error for invalid credentials
   - ✅ Password visibility toggle

3. **Session Management**
   - ✅ Logout successfully
   - ✅ Persist session after page refresh
   - ✅ Show user email in header when logged in

4. **Protected Routes**
   - ✅ Redirect to login when accessing protected route without auth
   - ✅ Protect estate plan detail routes

## Running Tests

### Prerequisites

1. Backend API must be running on `http://localhost:8000`
2. Frontend must be running on `http://localhost:3000` (or port specified in `playwright.config.ts`)
3. Database must be set up with migrations applied

### Run All Auth Tests

```bash
cd frontend/client-portal
npm run test:e2e -- tests/e2e/auth.spec.ts
```

### Run with UI Mode (Interactive)

```bash
npm run test:e2e:ui -- tests/e2e/auth.spec.ts
```

### Run in Debug Mode

```bash
npm run test:e2e:debug -- tests/e2e/auth.spec.ts
```

## Test Helpers

The `tests/helpers/auth.ts` file provides reusable authentication functions:

- `generateTestUser()` - Create a unique test user
- `registerUser()` - Register a user via UI
- `loginUser()` - Login a user via UI
- `registerAndLogin()` - Register and login in one step
- `logoutUser()` - Logout current user
- `clearAuthState()` - Clear all auth state
- `isLoggedIn()` - Check if user is logged in

### Example Usage

```typescript
import { registerAndLogin, generateTestUser } from '../helpers/auth';

test('should create estate plan when logged in', async ({ page }) => {
  // Register and login
  const user = await registerAndLogin(page);
  
  // Now test estate plan creation
  await page.goto('/');
  // ... rest of test
});
```

## Manual Testing Checklist

While E2E tests cover automated scenarios, manual testing should verify:

### Registration
- [ ] Registration form displays correctly
- [ ] All fields are required (email, password)
- [ ] Full name is optional
- [ ] Password must be at least 8 characters
- [ ] Email format validation works
- [ ] Success message appears after registration
- [ ] Redirects to login page after successful registration
- [ ] Error messages are clear and helpful

### Login
- [ ] Login form displays correctly
- [ ] Email and password fields are required
- [ ] Password visibility toggle works
- [ ] "Sign up" link navigates to registration
- [ ] Invalid credentials show error message
- [ ] Successful login redirects to dashboard
- [ ] User email appears in header after login

### Session Management
- [ ] Session persists after page refresh
- [ ] Session persists after closing and reopening browser tab
- [ ] Logout button is visible when logged in
- [ ] Logout redirects to login page
- [ ] After logout, protected routes redirect to login

### Protected Routes
- [ ] Home page (`/`) requires authentication
- [ ] Estate plan detail pages require authentication
- [ ] Unauthenticated users are redirected to login
- [ ] After login, users are redirected to originally requested page (if applicable)

## Known Issues

1. **Test Timing**: Some tests may need longer timeouts if backend is slow to respond
2. **Test User Cleanup**: Test users are created with unique emails but not automatically deleted
3. **Session Storage**: Tests clear localStorage/sessionStorage but may need to clear cookies explicitly

## Troubleshooting

### Tests Fail with "Failed to fetch"

- Ensure backend API is running on `http://localhost:8000`
- Check that CORS is configured correctly
- Verify `NEXT_PUBLIC_API_URL` environment variable

### Tests Fail with Timeout

- Increase timeout values in test configuration
- Check that frontend is running on expected port
- Verify database is accessible and migrations are applied

### Tests Fail with "Element not found"

- Check that selectors match current UI implementation
- Verify that UI components render correctly
- Check browser console for JavaScript errors

## Future Improvements

- [ ] Add tests for password reset flow
- [ ] Add tests for email verification flow
- [ ] Add tests for token refresh
- [ ] Add tests for concurrent sessions
- [ ] Add tests for session expiration
- [ ] Add performance tests for auth endpoints
- [ ] Add security tests (XSS, CSRF protection)

