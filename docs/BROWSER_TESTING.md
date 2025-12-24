# Browser Testing Guide

## Quick Test Checklist

### Prerequisites
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ PostgreSQL and Redis running (via Docker)

### Test Credentials
After running the test script, use these credentials:
- Email: `authtest[TIMESTAMP]@example.com`
- Password: `testpass123`

Or create your own test account.

---

## Test Flow

### 1. Registration Test

**Steps:**
1. Navigate to: http://localhost:3000/register
2. Fill in the form:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `testpass123` (at least 8 characters)
3. Click "Create Account"

**Expected:**
- ✅ Success toast: "Registration successful! Please sign in."
- ✅ Redirect to `/login` page
- ✅ No console errors

**If it fails:**
- Check browser console for errors
- Check backend logs
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify backend is running: `curl http://localhost:8000/health`

---

### 2. Login Test

**Steps:**
1. Navigate to: http://localhost:3000/login
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `testpass123`
3. Click "Sign In"

**Expected:**
- ✅ Success toast: "Login successful"
- ✅ Redirect to `/` (dashboard)
- ✅ User email shown in header
- ✅ No console errors

**If it fails:**
- Check browser console
- Check Network tab for API calls
- Verify JWT token is received
- Check backend logs

---

### 3. Protected Routes Test

**After Login:**

1. **Dashboard (`/`)**
   - ✅ Should show estate plans list (empty initially)
   - ✅ Should show user email in header
   - ✅ Should show "Sign Out" button

2. **Create Estate Plan**
   - ✅ Click "Create Estate Plan"
   - ✅ Fill form and submit
   - ✅ Should create and show in list
   - ✅ Should automatically set `user_id`

3. **Estate Plan Detail (`/estate-plans/[id]`)**
   - ✅ Click on an estate plan
   - ✅ Should show details page
   - ✅ Should allow adding beneficiaries
   - ✅ Should allow adding timelock policies

---

### 4. Logout Test

**Steps:**
1. Click "Sign Out" button
2. Should redirect to `/login`

**Expected:**
- ✅ Redirect to login page
- ✅ Cannot access protected routes
- ✅ Session cleared

---

## Debugging

### Check Backend
```bash
# Health check
curl http://localhost:8000/health

# Test registration
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456","full_name":"Test"}'

# Test login
curl -X POST http://localhost:8000/api/v1/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123456"
```

### Check Frontend
```bash
# Verify environment variables
cd frontend/client-portal
cat .env.local

# Should have:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXTAUTH_SECRET=...
# NEXTAUTH_URL=http://localhost:3000
```

### Browser Console
- Open DevTools (F12)
- Check Console tab for errors
- Check Network tab for failed requests
- Look for CORS errors
- Look for 401/403 errors

---

## Common Issues

### "Failed to fetch"
- **Cause**: Backend not running or wrong URL
- **Fix**: Check backend is running, verify `NEXT_PUBLIC_API_URL`

### "Invalid email or password"
- **Cause**: Wrong credentials or user doesn't exist
- **Fix**: Register first, then login

### "Unexpected end of JSON input"
- **Cause**: NextAuth session endpoint issue
- **Fix**: Check `NEXTAUTH_SECRET` is set, restart frontend

### CORS errors
- **Cause**: Backend CORS not configured for frontend URL
- **Fix**: Check `CORS_ORIGINS` in backend `.env`

### 401 Unauthorized
- **Cause**: Token expired or invalid
- **Fix**: Login again to get new token

---

## Automated Testing

Run the test script:
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
./scripts/test_auth_flow.sh
```

This will:
- ✅ Test backend health
- ✅ Test registration
- ✅ Test login
- ✅ Test protected endpoints
- ✅ Create test user credentials

---

**Last Updated**: December 2024

