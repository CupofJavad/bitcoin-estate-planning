#!/bin/bash
# Interactive Lunaverse Deployment Script
# Run this script on the Lunaverse server directly (after SSH)

set -e

echo "🚀 Bitcoin Estate Planning - Lunaverse Deployment"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker is not installed${NC}"
    echo "Please install Docker first:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install -y docker.io docker-compose"
    echo "  sudo usermod -aG docker $USER"
    echo "  newgrp docker"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if user can run docker
if ! docker ps &> /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Cannot run docker without sudo${NC}"
    echo "Please add yourself to docker group:"
    echo "  sudo usermod -aG docker $USER"
    echo "  newgrp docker"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed and accessible${NC}"

# Determine project directory
if [ -f "infra/docker/docker-compose.prod.yml" ]; then
    PROJECT_DIR=$(pwd)
    echo -e "${GREEN}✅ Found project in current directory${NC}"
elif [ -d "$HOME/bitcoin-estate-planning" ]; then
    PROJECT_DIR="$HOME/bitcoin-estate-planning"
    cd $PROJECT_DIR
    echo -e "${GREEN}✅ Found project in home directory${NC}"
elif [ -d "/opt/bitcoin-estate-planning" ]; then
    PROJECT_DIR="/opt/bitcoin-estate-planning"
    cd $PROJECT_DIR
    echo -e "${GREEN}✅ Found project in /opt${NC}"
else
    echo -e "${YELLOW}⚠️  Project not found. Cloning...${NC}"
    PROJECT_DIR="$HOME/bitcoin-estate-planning"
    cd $HOME
    git clone https://github.com/CupofJavad/bitcoin-estate-planning.git
    cd bitcoin-estate-planning
    git checkout feature/v2-core-enhancements
    echo -e "${GREEN}✅ Repository cloned${NC}"
fi

echo "📁 Project directory: $PROJECT_DIR"
cd $PROJECT_DIR

# Update repository
echo ""
echo "📥 Updating repository..."
git fetch origin
git checkout feature/v2-core-enhancements 2>/dev/null || git checkout -b feature/v2-core-enhancements origin/feature/v2-core-enhancements
git pull origin feature/v2-core-enhancements || echo "Already up to date"
echo -e "${GREEN}✅ Repository updated${NC}"

# Navigate to docker directory
cd infra/docker

# Create .env.prod if it doesn't exist
if [ ! -f ".env.prod" ]; then
    echo ""
    echo "📝 Creating .env.prod file..."
    
    # Generate secure passwords
    POSTGRES_PASS=$(openssl rand -base64 24)
    SECRET_KEY=$(openssl rand -base64 32)
    NEXTAUTH_SECRET=$(openssl rand -base64 32)
    
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
    
    echo -e "${GREEN}✅ Created .env.prod with generated passwords${NC}"
    echo ""
    echo "Generated passwords saved to .env.prod"
else
    echo -e "${GREEN}✅ .env.prod already exists${NC}"
fi

# Create SSL directory
if [ ! -d "ssl" ]; then
    echo ""
    echo "🔐 Creating SSL directory and self-signed certificate..."
    mkdir -p ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=lunaverse" 2>/dev/null || true
    echo -e "${GREEN}✅ SSL certificates created${NC}"
fi

# Stop existing services
echo ""
echo "🛑 Stopping existing services (if any)..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod down 2>/dev/null || true

# Build and start services
echo ""
echo "🔨 Building and starting services..."
echo "   This may take 5-10 minutes on first build..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for services
echo ""
echo "⏳ Waiting for services to start..."
sleep 30

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.prod.yml ps

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
sleep 5
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || {
    echo -e "${YELLOW}⚠️  Retrying migrations...${NC}"
    sleep 10
    docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
}

# Seed demo data
echo ""
echo "🌱 Seeding demo data..."
docker-compose -f docker-compose.prod.yml exec -T backend python scripts/seed_demo_data.py || {
    echo -e "${YELLOW}⚠️  Demo data seeding failed - check logs${NC}"
}

# Health checks
echo ""
echo "🏥 Running health checks..."
sleep 10

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    echo "   Check logs: docker-compose -f docker-compose.prod.yml logs backend"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is healthy${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
    echo "   Check logs: docker-compose -f docker-compose.prod.yml logs frontend"
fi

# Final summary
echo ""
echo "=================================================="
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo "🌐 Access your application:"
echo "  - Frontend: http://100.80.191.90:3000"
echo "  - Backend API: http://100.80.191.90:8000"
echo "  - API Docs: http://100.80.191.90:8000/docs"
echo ""
echo "🔑 Demo User (if seeded):"
echo "  - Email: demo@example.com"
echo "  - Password: demo123456"
echo ""
echo "📝 Useful Commands:"
echo "  - View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  - Restart: docker-compose -f docker-compose.prod.yml restart"
echo "  - Stop: docker-compose -f docker-compose.prod.yml down"
echo "  - Status: docker-compose -f docker-compose.prod.yml ps"
echo ""

