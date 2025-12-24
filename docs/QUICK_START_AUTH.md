# Quick Start Guide - Authentication Enabled

## Overview
This guide will help you get the application running with the new authentication system.

**Status**: ✅ Database migration complete - Ready to test!

---

## Prerequisites

1. **Docker Compose** - For PostgreSQL and Redis
2. **Python 3.12+** - For backend
3. **Node.js 18+** - For frontend
4. **Environment Variables** - Configured in `.env` files

---

## Step 1: Start Infrastructure Services

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
docker-compose -f infra/docker/docker-compose.yml up -d
```

**Verify services are running:**
```bash
docker-compose -f infra/docker/docker-compose.yml ps
```

You should see `postgres` and `redis` services running.

---

## Step 2: Configure Backend Environment

**Create backend `.env` file** (if it doesn't exist):
```bash
cd backend
cp env.example .env
```

**Edit `.env` and set these required variables:**
```env
# Secret key for JWT tokens (generate a random string)
SECRET_KEY=your-secret-key-here-minimum-32-characters-long

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=bitcoin_estate
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-postgres-password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# CORS (frontend URL)
CORS_ORIGINS=http://localhost:3000
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Step 3: Start Backend Server

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/backend
source .venv/bin/activate

# Verify database connection
python -c "from app.core.database import engine; print('✓ Database connection OK')"

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test the API:**
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Auth endpoints: http://localhost:8000/api/v1/auth/register

---

## Step 4: Configure Frontend Environment

**Create frontend `.env.local` file:**
```bash
cd frontend/client-portal
cp env.example .env.local
```

**Edit `.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-nextauth-secret-here
NEXTAUTH_URL=http://localhost:3000
```

**Generate NEXTAUTH_SECRET:**
```bash
openssl rand -base64 32
```

---

## Step 5: Install Frontend Dependencies

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/frontend/client-portal
npm install
```

**This will install:**
- NextAuth.js (authentication)
- All other dependencies

---

## Step 6: Start Frontend Server

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/frontend/client-portal
npm run dev
```

**Expected output:**
```
▲ Next.js 15.0.0
- Local:        http://localhost:3000
- ready started server on 0.0.0.0:3000
```

---

## Step 7: Test Authentication Flow

### 7.1 Register a New User

1. Navigate to: http://localhost:3000/register
2. Fill in the form:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123` (at least 8 characters)
3. Click "Create Account"
4. You should be redirected to `/login`

### 7.2 Login

1. Navigate to: http://localhost:3000/login
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Sign In"
4. You should be redirected to `/` (dashboard)

### 7.3 Test Protected Routes

1. **Dashboard** (`/`) - Should show estate plans (empty initially)
2. **Estate Plans** (`/estate-plans/[id]`) - Should require authentication
3. **Create Estate Plan** - Should work and automatically set `user_id`

### 7.4 Test API Endpoints

**Register (via API):**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api@example.com",
    "password": "password123",
    "full_name": "API User"
  }'
```

**Login (via API):**
```bash
curl -X POST http://localhost:8000/api/v1/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=api@example.com&password=password123"
```

**Get Current User (requires auth):**
```bash
# Use the access_token from login response
curl http://localhost:8000/api/v1/auth/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Troubleshooting

### Backend Issues

**Issue: "PermissionError: [Errno 1] Operation not permitted: '.env'"**
- Solution: Check file permissions: `chmod 644 backend/.env`
- Or create the file manually with proper permissions

**Issue: "Database connection failed"**
- Solution: Ensure PostgreSQL is running: `docker-compose -f infra/docker/docker-compose.yml ps`
- Check database credentials in `.env`

**Issue: "ModuleNotFoundError: No module named 'fastapi_users'"**
- Solution: Activate virtual environment and reinstall:
  ```bash
  source .venv/bin/activate
  pip install -e ".[dev]"
  ```

### Frontend Issues

**Issue: "next-auth not found"**
- Solution: Install dependencies: `npm install`

**Issue: "Failed to fetch" when calling API**
- Solution: 
  - Check backend is running on port 8000
  - Check `NEXT_PUBLIC_API_URL` in `.env.local`
  - Check CORS settings in backend `.env`

**Issue: "Redirect loop" on login**
- Solution: Check `NEXTAUTH_URL` matches your frontend URL

### Database Issues

**Issue: "Table 'users' already exists"**
- Solution: Migration already applied, this is normal
- Check migration status: `alembic current`

**Issue: "Migration not found"**
- Solution: Run migration: `alembic upgrade head`

---

## Verification Checklist

- [ ] PostgreSQL is running
- [ ] Redis is running
- [ ] Backend `.env` is configured
- [ ] Frontend `.env.local` is configured
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Can access http://localhost:3000
- [ ] Can register a new user
- [ ] Can login with registered user
- [ ] Can access protected routes
- [ ] Can create estate plan (automatically uses authenticated user)

---

## Next Steps

After successful setup:

1. **Test Complete Flow:**
   - Register → Login → Create Estate Plan → Add Beneficiaries → Add Timelock Policies

2. **Test Security:**
   - Try accessing another user's estate plans (should fail)
   - Try API calls without authentication (should fail)

3. **Review API Documentation:**
   - Visit http://localhost:8000/docs
   - Test endpoints interactively

---

**Last Updated**: December 2024  
**Status**: ✅ Ready for testing

