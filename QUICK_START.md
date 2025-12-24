# 🚀 Quick Start Guide

## One-Command Setup

### 1. Setup Environment Files
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
./scripts/setup-env.sh
```

This will:
- Create `backend/.env` with generated `SECRET_KEY`
- Create `frontend/client-portal/.env.local` with generated `NEXTAUTH_SECRET`
- Configure all required environment variables

### 2. Start Infrastructure Services
```bash
./scripts/start-all.sh
```

This will:
- Start PostgreSQL database
- Start Redis cache
- Verify services are running

### 3. Start Backend (Terminal 2)
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### 4. Start Frontend (Terminal 3)
```bash
cd frontend/client-portal
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## Test the Application

1. **Open Browser**: http://localhost:3000
2. **Register**: Click "Register" or go to http://localhost:3000/register
   - Fill in: Full Name, Email, Password
3. **Login**: After registration, login with your credentials
4. **Dashboard**: You'll see the estate planning dashboard
5. **Create Estate Plan**: Click "Create Estate Plan" button

---

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running: `docker-compose -f infra/docker/docker-compose.yml ps`
- Check `.env` file exists: `ls backend/.env`
- Check database connection in `.env`

### Frontend won't start
- Check `node_modules` installed: `npm install`
- Check `.env.local` exists: `ls frontend/client-portal/.env.local`
- Check `NEXT_PUBLIC_API_URL` matches backend URL

### Can't connect to database
- Start Docker services: `./scripts/start-all.sh`
- Check PostgreSQL logs: `docker-compose -f infra/docker/docker-compose.yml logs postgres`

---

## Manual Setup (Alternative)

If scripts don't work, follow the detailed guide:
- **Quick Start**: `START_HERE_AUTH.md`
- **Detailed Guide**: `docs/QUICK_START_AUTH.md`
- **Setup Checklist**: `SETUP_CHECKLIST.md`

---

**Last Updated**: December 2024

