#!/bin/bash
# Remote Deployment Script for Lunaverse
# Run this from your MacBook - it will SSH to Lunaverse and deploy

set -e

echo "🚀 Bitcoin Estate Planning - Remote Lunaverse Deployment"
echo "========================================================"
echo ""

# Server details
LUNAVERSE_HOST="100.80.191.90"
LUNAVERSE_USER="luna"
LUNAVERSE_PORT="22"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "📡 Connecting to Lunaverse server..."
echo "   Host: $LUNAVERSE_HOST"
echo "   User: $LUNAVERSE_USER"
echo ""

# Check if SSH key is available
if [ -f "$HOME/.ssh/id_rsa" ] || [ -f "$HOME/.ssh/id_ed25519" ]; then
    echo -e "${GREEN}✅ SSH key found${NC}"
    SSH_CMD="ssh -o StrictHostKeyChecking=no $LUNAVERSE_USER@$LUNAVERSE_HOST"
else
    echo -e "${YELLOW}⚠️  No SSH key found - you'll need to enter password${NC}"
    SSH_CMD="ssh -o StrictHostKeyChecking=no $LUNAVERSE_USER@$LUNAVERSE_HOST"
fi

# Create deployment script to run on server
DEPLOY_SCRIPT=$(cat << 'DEPLOYEOF'
#!/bin/bash
set -e

echo "🚀 Starting deployment on Lunaverse server..."
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo usermod -aG docker $USER
    echo "⚠️  Docker installed. Please log out and back in, then run deployment again."
    exit 0
fi

# Check if user can run docker
if ! docker ps &> /dev/null 2>&1; then
    echo "⚠️  Adding user to docker group..."
    sudo usermod -aG docker $USER
    echo "⚠️  Please run: newgrp docker"
    echo "Then run this script again."
    exit 0
fi

# Determine project directory
if [ -d "$HOME/bitcoin-estate-planning" ]; then
    PROJECT_DIR="$HOME/bitcoin-estate-planning"
    cd $PROJECT_DIR
    echo "📥 Updating existing repository..."
    git fetch origin
    git checkout feature/v2-core-enhancements 2>/dev/null || git checkout -b feature/v2-core-enhancements origin/feature/v2-core-enhancements
    git pull origin feature/v2-core-enhancements || echo "Already up to date"
elif [ -d "/opt/bitcoin-estate-planning" ]; then
    PROJECT_DIR="/opt/bitcoin-estate-planning"
    cd $PROJECT_DIR
    echo "📥 Updating existing repository..."
    git fetch origin
    git checkout feature/v2-core-enhancements 2>/dev/null || git checkout -b feature/v2-core-enhancements origin/feature/v2-core-enhancements
    git pull origin feature/v2-core-enhancements || echo "Already up to date"
else
    echo "📥 Cloning repository..."
    PROJECT_DIR="$HOME/bitcoin-estate-planning"
    cd $HOME
    git clone https://github.com/CupofJavad/bitcoin-estate-planning.git
    cd bitcoin-estate-planning
    git checkout feature/v2-core-enhancements
fi

echo "✅ Project directory: $PROJECT_DIR"
cd $PROJECT_DIR

# Navigate to docker directory
cd infra/docker

# Create .env.prod if it doesn't exist
if [ ! -f ".env.prod" ]; then
    echo "📝 Creating .env.prod file..."
    if [ -f "../CREATE_ENV_PROD.sh" ]; then
        bash ../CREATE_ENV_PROD.sh
    else
        # Create basic .env.prod
        cat > .env.prod << 'ENVEOF'
# Database Configuration
POSTGRES_DB=bitcoin_estate
POSTGRES_USER=postgres
POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD

# Backend Configuration
SECRET_KEY=CHANGE_ME_GENERATE_SECRET_KEY
BITCOIN_NETWORK=testnet
CORS_ORIGINS=http://100.80.191.90,http://100.80.191.90:3000,http://localhost:3000

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://100.80.191.90:8000/api
NEXTAUTH_SECRET=CHANGE_ME_GENERATE_SECRET_KEY
NEXTAUTH_URL=http://100.80.191.90

# Redis
REDIS_URL=redis://redis:6379/0
ENVEOF
    fi
    
    echo ""
    echo "⚠️  IMPORTANT: Edit .env.prod and set:"
    echo "   - POSTGRES_PASSWORD (generate: openssl rand -base64 24)"
    echo "   - SECRET_KEY (generate: openssl rand -base64 32)"
    echo "   - NEXTAUTH_SECRET (generate: openssl rand -base64 32)"
    echo ""
    echo "Generated values:"
    echo "POSTGRES_PASSWORD=$(openssl rand -base64 24)"
    echo "SECRET_KEY=$(openssl rand -base64 32)"
    echo "NEXTAUTH_SECRET=$(openssl rand -base64 32)"
    echo ""
    read -p "Press Enter after updating .env.prod with the generated values above..."
fi

# Create SSL directory
if [ ! -d "ssl" ]; then
    echo "🔐 Creating SSL directory..."
    mkdir -p ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=lunaverse" 2>/dev/null || true
fi

# Stop existing services
echo ""
echo "🛑 Stopping existing services (if any)..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod down 2>/dev/null || true

# Build and start
echo ""
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for services
echo ""
echo "⏳ Waiting for services to start..."
sleep 25

# Check status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.prod.yml ps

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
sleep 5
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || {
    echo "⚠️  Retrying migrations..."
    sleep 10
    docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
}

# Seed demo data
echo ""
echo "🌱 Seeding demo data..."
docker-compose -f docker-compose.prod.yml exec -T backend python scripts/seed_demo_data.py || {
    echo "⚠️  Demo data seeding failed - check logs"
}

# Health checks
echo ""
echo "🏥 Running health checks..."
sleep 10

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
fi

echo ""
echo "=========================================================="
echo "✅ Deployment Complete!"
echo ""
echo "🌐 Access your application:"
echo "  - Frontend: http://100.80.191.90:3000"
echo "  - Backend API: http://100.80.191.90:8000"
echo "  - API Docs: http://100.80.191.90:8000/docs"
echo ""
echo "🔑 Demo User:"
echo "  - Email: demo@example.com"
echo "  - Password: demo123456"
echo ""
DEPLOYEOF
)

# Copy deployment script to server and execute
echo "📤 Uploading deployment script to server..."
echo "$DEPLOY_SCRIPT" | $SSH_CMD "bash -s" 2>&1

echo ""
echo "✅ Deployment process initiated!"
echo ""
echo "📝 If you see any errors, check:"
echo "   - SSH connection is working"
echo "   - Docker is installed on server"
echo "   - User has docker permissions"
echo ""
echo "📚 For manual deployment, see: docs/LUNAVERSE_DEPLOY_NOW.md"

