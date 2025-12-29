# Lunaverse Deployment - Quick Start Guide

**Deploy the latest version (feature/v2-core-enhancements) to your Lunaverse server.**

## 🚀 Quick Deployment (5 Steps)

### Step 1: Connect to Lunaverse Server

```bash
# Via Tailscale (recommended)
ssh -p 22 luna@100.80.191.90

# Or via direct IP
ssh -p 22 luna@192.168.1.172
```

### Step 2: Clone/Update Repository

```bash
# If repository doesn't exist
cd /opt
git clone https://github.com/CupofJavad/bitcoin-estate-planning.git
cd bitcoin-estate-planning

# If repository exists, update it
cd /opt/bitcoin-estate-planning
git fetch origin
git checkout feature/v2-core-enhancements
git pull origin feature/v2-core-enhancements
```

### Step 3: Create Production Environment File

```bash
cd /opt/bitcoin-estate-planning/infra/docker

# Run the environment file creation script
bash CREATE_ENV_PROD.sh

# Edit the file with your actual values
nano .env.prod
```

**Required values to update in `.env.prod`:**
- `POSTGRES_PASSWORD` - Generate: `openssl rand -base64 24`
- `SECRET_KEY` - Generate: `openssl rand -base64 32`
- `NEXTAUTH_SECRET` - Generate: `openssl rand -base64 32`
- `LUNAVERSE_SSH_PASSWORD` - Your actual SSH password
- `OPENAI_API_KEY` - If you want chatbot functionality
- Update URLs to use your Tailscale IP or domain

### Step 4: Deploy Services

```bash
cd /opt/bitcoin-estate-planning/infra/docker

# Option A: Use automated deployment script
cd /opt/bitcoin-estate-planning
bash scripts/deploy-to-lunaverse.sh

# Option B: Manual deployment
cd /opt/bitcoin-estate-planning/infra/docker
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

### Step 5: Run Database Migrations

```bash
cd /opt/bitcoin-estate-planning/infra/docker

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Seed demo data (optional)
docker-compose -f docker-compose.prod.yml exec backend python scripts/seed_demo_data.py
```

## ✅ Verify Deployment

```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🌐 Access Your Application

**Via Tailscale:**
- Frontend: `http://100.80.191.90:3000` or `http://100.80.191.90`
- Backend API: `http://100.80.191.90:8000`
- API Docs: `http://100.80.191.90:8000/docs`

**Via Direct IP:**
- Frontend: `http://192.168.1.172:3000` or `http://192.168.1.172`
- Backend API: `http://192.168.1.172:8000`
- API Docs: `http://192.168.1.172:8000/docs`

## 🔑 Demo User Credentials

After seeding demo data:
- **Email:** `demo@example.com`
- **Password:** `demo123456`

## 📝 Important Notes

1. **Ports:** Make sure ports 80, 443, 3000, and 8000 are accessible
2. **Firewall:** Configure firewall to allow these ports
3. **SSL:** For production, set up SSL certificates (see full guide)
4. **Backups:** Set up automated database backups
5. **Updates:** Pull latest code and redeploy when needed

## 🆘 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check specific service
docker-compose -f docker-compose.prod.yml logs backend
```

### Database Issues
```bash
# Check database is running
docker-compose -f docker-compose.prod.yml ps postgres

# Test connection
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d bitcoin_estate
```

### Frontend Can't Connect to Backend
- Verify `NEXT_PUBLIC_API_URL` in `.env.prod` matches your backend URL
- Check CORS configuration
- Verify backend is running: `curl http://localhost:8000/health`

## 📚 Full Documentation

- **Complete Guide:** [LUNAVERSE_DEPLOYMENT.md](LUNAVERSE_DEPLOYMENT.md)
- **Deployment Decision:** [DEPLOYMENT_DECISION.md](DEPLOYMENT_DECISION.md)

---

**Last Updated:** December 29, 2024
