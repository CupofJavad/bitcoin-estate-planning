# Infrastructure & Deployment FAQ

## 1. Server & Digital Ocean - Hosting Configuration

### Current Status
**The Bitcoin Estate Planning Platform is currently configured for LOCAL DEVELOPMENT only.** There is no active production deployment configured yet.

### What's Configured:

#### Development (Local - Your MacBook)
- **Backend**: Running directly via `uvicorn` (not Docker)
- **Frontend**: Running directly via `npm run dev` (not Docker)
- **Database**: PostgreSQL in Docker container (via `docker-compose.yml`)
- **Redis**: Redis in Docker container (via `docker-compose.yml`)

#### Production Deployment Options (Not Yet Deployed)
The project includes deployment configurations for multiple platforms:

1. **Self-Hosted VPS** (e.g., your Lunaverse server)
   - Uses `docker-compose.prod.yml`
   - Includes: Backend, Frontend, PostgreSQL, Redis, Nginx
   - Would run on your Lunaverse server

2. **DigitalOcean App Platform** (mentioned in `DEPLOYMENT.md`)
   - Can deploy backend and frontend as separate apps
   - Can use DigitalOcean managed PostgreSQL
   - Can use DigitalOcean managed Redis

3. **Other Platforms** (Railway, AWS, etc.)
   - Generic Docker-based deployment

### Recommendation: Choose One Approach

**Option A: Deploy to Lunaverse Server (Self-Hosted)**
- Use your existing Lunaverse server
- Run everything via Docker Compose
- You manage the server, updates, backups

**Option B: Deploy to DigitalOcean**
- Use DigitalOcean App Platform for backend/frontend
- Use DigitalOcean Managed Database for PostgreSQL
- Use DigitalOcean Managed Redis
- More managed, less server maintenance

**Option C: Hybrid**
- Backend/Frontend on DigitalOcean App Platform
- Database on DigitalOcean Managed Database
- Or: Backend/Frontend on Lunaverse, Database on DigitalOcean

### Current Configuration Files
- `infra/docker/docker-compose.yml` - Development (PostgreSQL + Redis only)
- `infra/docker/docker-compose.prod.yml` - Production (Full stack)
- `.github/workflows/deploy.yml` - CI/CD (needs configuration for your server)

---

## 2. Docker - Do I Need It Running?

### For Local Development: **Partially**

**What You Currently Need:**
- ✅ **Docker Desktop must be running** for:
  - PostgreSQL database (port 5432)
  - Redis cache (port 6379)
  
**What You DON'T Need Docker For:**
- ❌ Backend (running directly via `uvicorn`)
- ❌ Frontend (running directly via `npm run dev`)

### Current Setup (What You're Using Now)
```bash
# Terminal 1: Start infrastructure (Docker required)
docker-compose -f infra/docker/docker-compose.yml up -d

# Terminal 2: Backend (no Docker)
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload

# Terminal 3: Frontend (no Docker)
cd frontend/client-portal && npm run dev
```

### Alternative: Full Docker Development
If you want to run everything in Docker (optional):
```bash
# Would need a docker-compose.dev.yml with backend and frontend
# Currently not configured - would need to be created
```

### For Production Deployment: **Yes, Required**
- Production uses Docker Compose
- All services run in containers
- Requires Docker and Docker Compose on the server

### Answer: **Yes, keep Docker Desktop running** for local development because PostgreSQL and Redis run in containers.

---

## 3. Tailscale - Is It Needed?

### Current Status: **Not Required for Local Development**

**Tailscale is NOT needed for:**
- ✅ Local development on your MacBook
- ✅ Running the app at `localhost:3000` and `localhost:8000`
- ✅ Database connections (PostgreSQL is in local Docker)

**Tailscale IS used for:**
- 🔗 Accessing your Lunaverse server remotely
- 🔗 SSH access to Lunaverse via Tailscale hostname
- 🔗 Future production deployment if you deploy to Lunaverse

### Is Tailscale Interfering?

**Unlikely, but possible issues:**
1. **Port Conflicts**: If Tailscale is using ports 3000, 8000, 5432, or 6379
   - Check: `lsof -i :3000` and `lsof -i :8000`
   - Solution: Change ports in your app if needed

2. **Network Routing**: Tailscale might route localhost traffic
   - Check: `tailscale status`
   - Solution: Exclude localhost from Tailscale routing

3. **DNS Resolution**: Tailscale DNS might interfere
   - Check: `scutil --dns | grep tailscale`
   - Solution: Disable Tailscale DNS for localhost

### Testing if Tailscale is Causing Issues

1. **Temporarily disconnect Tailscale:**
   ```bash
   # macOS: System Settings > Network > Tailscale > Disconnect
   # Or: tailscale down
   ```

2. **Test the app:**
   - Try accessing `http://localhost:3000`
   - Check if backend responds at `http://localhost:8000`

3. **If it works without Tailscale:**
   - Tailscale might be interfering
   - Configure Tailscale to exclude localhost

### Recommendation
- **For local development**: You can keep Tailscale running, but it's not required
- **If you see connection issues**: Try disconnecting Tailscale temporarily
- **For production on Lunaverse**: Tailscale is useful for server access

### Additional Configuration Needed?
**No additional app configuration needed** for Tailscale. The app doesn't know or care about Tailscale - it just uses standard localhost connections.

---

## 4. Application Status & Next Steps

### ✅ Current Status (December 2024)

#### What's Working:
- ✅ **Backend API**: FastAPI running on port 8000
- ✅ **Frontend UI**: Next.js running on port 3000
- ✅ **Database**: PostgreSQL in Docker, migrations applied
- ✅ **Authentication**: User registration and login working
- ✅ **Core Features**: Estate plans, beneficiaries, timelock policies
- ✅ **Bitcoin Integration**: Address validation and balance checking
- ✅ **Chatbot**: AI assistant integrated (requires OpenAI API key)
- ✅ **E2E Tests**: Playwright tests configured

#### What's Fixed (Just Now):
- ✅ Backend `UserManager.parse_id` method added
- ✅ NextAuth v5 handler export fixed
- ✅ File permissions for `.env` files fixed
- ✅ Backend and frontend both running successfully

### 📋 What's Remaining for Full Production Deployment

#### Phase 1: Environment Configuration
- [ ] Set up production environment variables
- [ ] Configure SSL certificates
- [ ] Set up domain name (if using custom domain)

#### Phase 2: Choose Deployment Target
- [ ] **Option A**: Configure Lunaverse server deployment
  - [ ] Install Docker and Docker Compose on server
  - [ ] Set up environment variables on server
  - [ ] Configure Nginx reverse proxy
  - [ ] Set up SSL (Let's Encrypt)
  
- [ ] **Option B**: Configure DigitalOcean deployment
  - [ ] Create DigitalOcean App Platform apps
  - [ ] Set up managed PostgreSQL database
  - [ ] Set up managed Redis
  - [ ] Configure environment variables
  - [ ] Set up custom domain

#### Phase 3: CI/CD Configuration
- [ ] Update `.github/workflows/deploy.yml` with your server details
- [ ] Configure deployment secrets in GitHub
- [ ] Test automated deployment

#### Phase 4: Production Readiness
- [ ] Set up database backups
- [ ] Configure monitoring and logging
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Performance testing
- [ ] Security audit

### 🚀 Quick Start: Get Latest Version Running Locally

**Right now, the app IS running!** Here's how to start it fresh:

```bash
# 1. Start infrastructure (Docker required)
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
docker-compose -f infra/docker/docker-compose.yml up -d

# 2. Start backend (Terminal 1)
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 3. Start frontend (Terminal 2)
cd frontend/client-portal
npm run dev

# 4. Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 📝 Next Steps Summary

**Immediate (Testing):**
1. ✅ App is running - test all features
2. ✅ Verify authentication works
3. ✅ Test estate plan creation
4. ✅ Test beneficiary management
5. ✅ Test timelock policies

**Short-term (Deployment Planning):**
1. Decide: Lunaverse server OR DigitalOcean
2. Set up production environment
3. Configure deployment scripts
4. Test production deployment

**Long-term (Production):**
1. Set up monitoring
2. Configure backups
3. Set up CI/CD
4. Performance optimization

---

## Summary

### Your Questions Answered:

1. **Server & Digital Ocean**: 
   - Currently: Local development only
   - Lunaverse: Can host full stack via Docker
   - DigitalOcean: Can host via App Platform + Managed DB
   - **Action**: Choose one deployment target

2. **Docker**: 
   - **Yes, keep running** for PostgreSQL and Redis
   - Backend/Frontend run directly (not in Docker for dev)
   - Production requires full Docker setup

3. **Tailscale**: 
   - **Not required** for local development
   - Useful for accessing Lunaverse server
   - **Unlikely to interfere**, but test if you see issues

4. **Application Status**: 
   - ✅ **Currently working** and ready for testing
   - ✅ All core features implemented
   - 📋 Production deployment needs configuration
   - 📋 Choose deployment target (Lunaverse or DigitalOcean)

---

**Last Updated**: December 28, 2024

