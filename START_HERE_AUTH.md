# 🚀 Start Here - Authentication Testing

## ✅ Status: Ready to Test!

The authentication system is **fully implemented** and ready for testing. The database migration has been successfully applied.

---

## Quick Start (3 Terminals)

### Terminal 1: Start Infrastructure
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
docker-compose -f infra/docker/docker-compose.yml up -d
```

### Terminal 2: Start Backend
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/backend
source .venv/bin/activate

# Make sure .env file exists with SECRET_KEY
# If not, copy from env.example and configure

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 3: Start Frontend
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/frontend/client-portal

# Install dependencies if needed
npm install

# Make sure .env.local exists with:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXTAUTH_SECRET=<generate with: openssl rand -base64 32>
# NEXTAUTH_URL=http://localhost:3000

npm run dev
```

---

## Test the Authentication

1. **Open Browser**: http://localhost:3000
2. **You'll be redirected to**: http://localhost:3000/login (protected route)
3. **Click "Sign up"** or go to: http://localhost:3000/register
4. **Create an account**:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123`
5. **Login** with your credentials
6. **You'll see the dashboard** with your user email in the header
7. **Try creating an estate plan** - it will automatically use your user ID!

---

## What's New

### ✅ Authentication Features
- User registration
- User login with JWT tokens
- Protected routes (redirects to login if not authenticated)
- User-specific data (users can only see their own estate plans)
- Logout functionality
- Session management

### ✅ Security
- All API endpoints require authentication
- Users can only access their own data
- JWT tokens expire after 30 minutes
- Passwords are hashed with bcrypt

---

## API Endpoints

**Public (No Auth Required):**
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/jwt/login` - Login

**Protected (Auth Required):**
- `GET /api/v1/auth/users/me` - Get current user
- `GET /api/v1/estate-plans` - List user's estate plans
- `POST /api/v1/estate-plans` - Create estate plan
- All other endpoints require authentication

---

## Documentation

- **Quick Start**: `docs/QUICK_START_AUTH.md`
- **Testing Guide**: `docs/TESTING_AUTH.md`
- **Progress**: `docs/PHASE_2_PROGRESS.md`
- **Migration Instructions**: `docs/MIGRATION_INSTRUCTIONS.md`

---

## Need Help?

Check the troubleshooting sections in:
- `docs/QUICK_START_AUTH.md`
- `docs/TESTING_AUTH.md`

---

**🎉 Enjoy testing the new authentication system!**

