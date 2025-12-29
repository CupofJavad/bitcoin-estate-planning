# Deploy to Lunaverse - Step by Step

## Quick Deployment (Copy & Paste)

### Step 1: Connect to Your Lunaverse Server

```bash
ssh luna@100.80.191.90
```

Enter your SSH password when prompted.

### Step 2: Run These Commands on the Server

Once connected, copy and paste this entire block:

```bash
# Install Docker if needed
if ! command -v docker &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo usermod -aG docker $USER
    newgrp docker
fi

# Clone or update repository
if [ -d "$HOME/bitcoin-estate-planning" ]; then
    cd ~/bitcoin-estate-planning
    git fetch origin
    git checkout feature/v2-core-enhancements
    git pull origin feature/v2-core-enhancements
else
    cd ~
    git clone https://github.com/CupofJavad/bitcoin-estate-planning.git
    cd bitcoin-estate-planning
    git checkout feature/v2-core-enhancements
fi

# Navigate to docker directory
cd infra/docker

# Generate secure passwords
POSTGRES_PASS=$(openssl rand -base64 24)
SECRET_KEY=$(openssl rand -base64 32)
NEXTAUTH_SECRET=$(openssl rand -base64 32)

# Create .env.prod file
cat > .env.prod << EOF
# Database Configuration
POSTGRES_DB=bitcoin_estate
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${POSTGRES_PASS}

# Backend Configuration
SECRET_KEY=${SECRET_KEY}
BITCOIN_NETWORK=testnet
CORS_ORIGINS=http://100.80.191.90,http://100.80.191.90:3000,http://localhost:3000

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://100.80.191.90:8000/api
NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
NEXTAUTH_URL=http://100.80.191.90

# Redis
REDIS_URL=redis://redis:6379/0
EOF

# Create SSL directory and self-signed cert
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=lunaverse" 2>/dev/null || true

# Stop any existing services
docker-compose -f docker-compose.prod.yml --env-file .env.prod down 2>/dev/null || true

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 30

# Run migrations
echo "🗄️  Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

# Seed demo data
echo "🌱 Seeding demo data..."
docker-compose -f docker-compose.prod.yml exec -T backend python scripts/seed_demo_data.py

# Check status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.prod.yml ps

# Health checks
echo ""
echo "🏥 Health Checks:"
curl -f http://localhost:8000/health && echo " ✅ Backend healthy" || echo " ❌ Backend failed"
curl -f http://localhost:3000 && echo " ✅ Frontend healthy" || echo " ❌ Frontend failed"

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "🌐 Access your application:"
echo "  - Frontend: http://100.80.191.90:3000"
echo "  - Backend: http://100.80.191.90:8000"
echo "  - API Docs: http://100.80.191.90:8000/docs"
echo ""
echo "🔑 Demo User: demo@example.com / demo123456"
```

### Step 3: Verify Deployment

From your MacBook, test the deployment:

```bash
# Test backend
curl http://100.80.191.90:8000/health

# Test frontend
curl http://100.80.191.90:3000
```

## Alternative: Use the Deployment Script

If you prefer, you can use the automated script:

```bash
# On your MacBook
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
bash scripts/deploy-lunaverse-remote.sh
```

## Troubleshooting

### If Docker permission errors occur:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### If services won't start:
```bash
cd ~/bitcoin-estate-planning/infra/docker
docker-compose -f docker-compose.prod.yml logs
```

### If ports are not accessible:
```bash
# Check firewall
sudo ufw status
# Allow ports if needed
sudo ufw allow 3000/tcp
sudo ufw allow 8000/tcp
```

---

**Ready to deploy!** Just SSH to your server and run the commands above.

