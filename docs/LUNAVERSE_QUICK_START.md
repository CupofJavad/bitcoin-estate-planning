# Lunaverse Quick Start - Live Deployment

## Current Status
✅ Connected to Lunaverse server (100.80.191.90)
✅ Server specs: Ubuntu 24.04.3, 97.87GB disk, 9% memory usage
⚠️ Permission issue with `/opt` directory

## Solution: Use Home Directory

Since `/opt` requires root permissions, we'll deploy to your home directory instead.

### Step 1: Clone Repository to Home Directory

```bash
# On Lunaverse server (you're already connected)
cd ~
git clone https://github.com/CupofJavad/bitcoin-estate-planning.git
cd bitcoin-estate-planning
```

### Step 2: Check Docker Installation

```bash
# Check if Docker is installed
docker --version
docker-compose --version

# If not installed, install it:
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker

# Verify you can run docker without sudo
docker ps
```

### Step 3: Run Deployment Script

```bash
# Make script executable
chmod +x scripts/deploy-to-lunaverse.sh

# Run deployment
./scripts/deploy-to-lunaverse.sh
```

### Step 4: Manual Deployment (Alternative)

If the script doesn't work, follow these steps:

```bash
# Navigate to docker directory
cd ~/bitcoin-estate-planning/infra/docker

# Create .env.prod file
cat > .env.prod << 'EOF'
# Database Configuration
POSTGRES_DB=bitcoin_estate
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$(openssl rand -base64 24)

# Backend Configuration
SECRET_KEY=$(openssl rand -base64 32)
BITCOIN_NETWORK=testnet
CORS_ORIGINS=http://localhost:3000,http://100.80.191.90,https://100.80.191.90

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://100.80.191.90:8000/api
NEXTAUTH_SECRET=$(openssl rand -base64 32)
NEXTAUTH_URL=http://100.80.191.90
EOF

# Generate passwords (run these commands and update .env.prod)
openssl rand -base64 32  # For SECRET_KEY
openssl rand -base64 32  # For NEXTAUTH_SECRET
openssl rand -base64 24  # For POSTGRES_PASSWORD

# Edit .env.prod with the generated values
nano .env.prod

# Create SSL directory (for self-signed cert, or skip for HTTP)
mkdir -p ssl

# Generate self-signed certificate (for testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=lunaverse"

# Build and start services
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for services to start
sleep 15

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### Step 5: Verify Deployment

```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# View logs if needed
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 6: Access the Application

**From your MacBook:**
- Frontend: `http://100.80.191.90:3000` (if port is exposed)
- Backend API: `http://100.80.191.90:8000/docs`

**Note:** You may need to configure firewall rules to expose ports:
```bash
# Allow ports 80, 443, 3000, 8000
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 8000/tcp
sudo ufw enable
```

## Troubleshooting

### Permission Denied on /opt
**Solution:** Use home directory (`~`) instead of `/opt`

### Docker Permission Denied
**Solution:** Add user to docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Port Already in Use
**Solution:** Check what's using the port:
```bash
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000
```

### Services Won't Start
**Solution:** Check logs:
```bash
docker-compose -f docker-compose.prod.yml logs
```

## Next Steps After Deployment

1. **Set up backups** (see LUNAVERSE_DEPLOYMENT.md)
2. **Configure domain** (if you have one)
3. **Set up SSL** with Let's Encrypt (for production)
4. **Configure firewall** to expose necessary ports
5. **Set up monitoring** and log rotation

---

**Last Updated**: December 29, 2024

