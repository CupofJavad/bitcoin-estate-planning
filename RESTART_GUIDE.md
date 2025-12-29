# Quick Restart Guide

After closing your laptop or restarting, follow these steps to get the app running again.

## Quick Start (3 Steps)

### 1. Start Infrastructure Services (Docker)
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
docker-compose -f infra/docker/docker-compose.yml up -d
```

**Verify it's running:**
```bash
docker-compose -f infra/docker/docker-compose.yml ps
# Should show postgres and redis as "Up"
```

### 2. Start Backend (Terminal 1)
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Verify it's running:**
- Open: http://localhost:8000/health
- Should see: `{"status":"healthy"}`

### 3. Start Frontend (Terminal 2)
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/frontend/client-portal
npm run dev
```

**Verify it's running:**
- Open: http://localhost:3000
- Should see the login page

---

## Troubleshooting

### Docker containers not starting?
```bash
# Check Docker Desktop is running
# macOS: Open Docker Desktop app

# Restart containers
docker-compose -f infra/docker/docker-compose.yml down
docker-compose -f infra/docker/docker-compose.yml up -d
```

### Backend won't start?
```bash
# Check .env file exists
ls backend/.env

# Check file permissions
chmod 644 backend/.env

# Check database is running
docker-compose -f infra/docker/docker-compose.yml ps postgres
```

### Frontend won't start?
```bash
# Check .env.local exists
ls frontend/client-portal/.env.local

# Check file permissions
chmod 644 frontend/client-portal/.env.local

# Reinstall dependencies if needed
cd frontend/client-portal
npm install
```

### Port already in use?
```bash
# Check what's using the port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Kill process if needed (replace PID)
kill -9 <PID>
```

---

## Using Makefile (Alternative)

If you have the Makefile set up:
```bash
make start-services  # Start Docker containers
make dev-backend     # Start backend
make dev-frontend    # Start frontend
```

---

## Quick Status Check

```bash
# Check all services
curl http://localhost:8000/health && echo " ✓ Backend OK" || echo " ✗ Backend down"
curl http://localhost:3000 > /dev/null 2>&1 && echo " ✓ Frontend OK" || echo " ✗ Frontend down"
docker-compose -f infra/docker/docker-compose.yml ps | grep -q "Up" && echo " ✓ Docker OK" || echo " ✗ Docker down"
```

---

**Last Updated**: December 28, 2024

