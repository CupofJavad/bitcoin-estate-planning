# Troubleshooting Guide

## Current Issues & Solutions

### Issue 1: Frontend Running on Port 3004
**Problem**: Frontend automatically switched to port 3004 because 3000 is in use.

**Solution**: 
- Access frontend at: `http://localhost:3004`
- Or free port 3000: `kill -9 $(lsof -ti:3000)`

### Issue 2: NextAuth JSON Parsing Error
**Problem**: "Unexpected end of JSON input" in NextAuth.

**Solution**: ✅ Fixed
- Added proper JSON parsing with error handling
- Check for empty responses before parsing
- Added debug logging

### Issue 3: Next.js Build Error
**Problem**: "ENOENT: no such file or directory" for vendor chunks.

**Solution**: ✅ Fixed
- Cleared `.next` directory
- Restart frontend to rebuild

### Issue 4: Method Not Allowed (405)
**Problem**: Register endpoint returns "Method Not Allowed".

**Solution**: 
- ✅ Backend endpoint works (tested via curl)
- Check browser Network tab for actual request method
- Verify request is POST, not GET

---

## Step-by-Step Debugging

### 1. Check Backend is Running
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### 2. Test Registration Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456","full_name":"Test"}'
# Should return: User object with 201 status
```

### 3. Check Frontend Environment
```bash
cd frontend/client-portal
cat .env.local
# Should have:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXTAUTH_SECRET=...
# NEXTAUTH_URL=http://localhost:3004 (or 3000)
```

### 4. Check Browser Console
1. Open DevTools (F12)
2. Go to Console tab
3. Look for:
   - "API URL: http://localhost:8000/api/v1/auth/register"
   - "Registering with: {email: ..., hasPassword: true, ...}"
   - "Registration response status: 201"

### 5. Check Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Try registering
4. Find the `/api/v1/auth/register` request
5. Check:
   - **Request Method**: Should be `POST`
   - **Request URL**: Should be `http://localhost:8000/api/v1/auth/register`
   - **Request Payload**: Should have email, password, full_name
   - **Response Status**: Should be `201` or `200`
   - **Response Body**: Should be user object or error message

---

## Common Errors & Fixes

### "Failed to fetch"
- **Cause**: Backend not running or network issue
- **Fix**: 
  - Check backend: `curl http://localhost:8000/health`
  - Check backend logs
  - Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### "Method Not Allowed (405)"
- **Cause**: Wrong HTTP method or endpoint path
- **Fix**:
  - Verify endpoint: `/api/v1/auth/register` (not `/register/register`)
  - Check request method is `POST`
  - Check Network tab for actual request

### "Unexpected end of JSON input"
- **Cause**: Empty or invalid JSON response
- **Fix**: ✅ Already fixed in code
  - Check backend is returning valid JSON
  - Check Network tab for response body

### "CORS error"
- **Cause**: Backend CORS not configured for frontend URL
- **Fix**:
  - Add frontend URL to `CORS_ORIGINS` in backend `.env`
  - Include port: `http://localhost:3004` (if using 3004)
  - Restart backend after changing `.env`

### "401 Unauthorized"
- **Cause**: Invalid or expired token
- **Fix**: Login again to get new token

---

## Quick Test Commands

### Test Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"quicktest@example.com","password":"test123456","full_name":"Quick Test"}'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=quicktest@example.com&password=test123456"
```

### Run Full Test Suite
```bash
./scripts/test_auth_flow.sh
```

---

## Browser Testing Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running (check port: 3000 or 3004)
- [ ] `.env.local` configured correctly
- [ ] Browser DevTools open (F12)
- [ ] Console tab shows debug logs
- [ ] Network tab shows requests
- [ ] Try registration
- [ ] Check response in Network tab
- [ ] Check errors in Console tab

---

**Last Updated**: December 2024

