# Frontend Port Issue Fix

## Issue
Frontend is running on port **3004** instead of **3000** because port 3000 is already in use.

## Impact
- Frontend URL: `http://localhost:3004` (not 3000)
- NextAuth URL might need updating
- CORS might need updating if using port 3004

## Solutions

### Option 1: Use Port 3004 (Current)
If you want to keep using port 3004:

1. **Update `.env.local`:**
   ```env
   NEXTAUTH_URL=http://localhost:3004
   ```

2. **Update backend CORS** (if needed):
   ```env
   CORS_ORIGINS=http://localhost:3000,http://localhost:3004
   ```

3. **Access frontend at:** `http://localhost:3004`

### Option 2: Free Port 3000 (Recommended)
If you want to use the standard port 3000:

1. **Find what's using port 3000:**
   ```bash
   lsof -ti:3000
   ```

2. **Kill the process:**
   ```bash
   kill -9 $(lsof -ti:3000)
   ```

3. **Restart frontend:**
   ```bash
   cd frontend/client-portal
   npm run dev
   ```

4. **Frontend will now run on:** `http://localhost:3000`

## Current Status
- Frontend: `http://localhost:3004` ✅
- Backend: `http://localhost:8000` ✅
- CORS: Configured for both ports ✅

## Testing
Use the correct port when testing:
- Registration: `http://localhost:3004/register`
- Login: `http://localhost:3004/login`
- Dashboard: `http://localhost:3004/`

---

**Last Updated**: December 2024

