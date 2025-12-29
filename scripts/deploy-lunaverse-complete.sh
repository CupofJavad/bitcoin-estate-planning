#!/bin/bash
# Complete Lunaverse Deployment Script
# This script handles the full deployment process

set -e

echo "🚀 Bitcoin Estate Planning - Complete Lunaverse Deployment"
echo "=========================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're on the server or need to SSH
if [ -z "$LUNAVERSE_DEPLOY_LOCAL" ]; then
    echo -e "${YELLOW}📡 This script should be run on your Lunaverse server${NC}"
    echo ""
    echo "To deploy remotely, run from your MacBook:"
    echo "  ssh luna@100.80.191.90 'bash -s' < scripts/deploy-lunaverse-complete.sh"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Installing...${NC}"
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✅ Docker installed. Please log out and back in, then run this script again.${NC}"
    exit 0
fi

# Check if user can run docker without sudo
if ! docker ps &> /dev/null; then
    echo -e "${YELLOW}⚠️  Adding user to docker group...${NC}"
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✅ Added to docker group. Run: newgrp docker${NC}"
    echo "Then run this script again."
    exit 0
fi

# Determine project directory
if [ -f "infra/docker/docker-compose.prod.yml" ]; then
    PROJECT_DIR=$(pwd)
elif [ -d "/opt/bitcoin-estate-planning" ]; then
    PROJECT_DIR="/opt/bitcoin-estate-planning"
    cd $PROJECT_DIR
elif [ -d "$HOME/bitcoin-estate-planning" ]; then
    PROJECT_DIR="$HOME/bitcoin-estate-planning"
    cd $PROJECT_DIR
else
    echo -e "${YELLOW}⚠️  Project not found. Cloning...${NC}"
    PROJECT_DIR="$HOME/bitcoin-estate-planning"
    cd $HOME
    git clone https://github.com/CupofJavad/bitcoin-estate-planning.git
    cd bitcoin-estate-planning
    git checkout feature/v2-core-enhancements
fi

echo -e "${GREEN}✅ Project directory: $PROJECT_DIR${NC}"
cd $PROJECT_DIR

# Update repository
echo ""
echo "📥 Updating repository..."
git fetch origin
git checkout feature/v2-core-enhancements
git pull origin feature/v2-core-enhancements || echo "Already up to date"

# Navigate to docker directory
cd infra/docker

# Create .env.prod if it doesn't exist
if [ ! -f ".env.prod" ]; then
    echo ""
    echo "📝 Creating .env.prod file..."
    bash ../CREATE_ENV_PROD.sh
    
    echo ""
    echo -e "${YELLOW}⚠️  Please edit .env.prod with your actual values:${NC}"
    echo "  - POSTGRES_PASSWORD (generate: openssl rand -base64 24)"
    echo "  - SECRET_KEY (generate: openssl rand -base64 32)"
    echo "  - NEXTAUTH_SECRET (generate: openssl rand -base64 32)"
    echo "  - Update URLs to match your server"
    echo ""
    read -p "Press Enter after editing .env.prod..."
fi

# Create SSL directory if needed
if [ ! -d "ssl" ]; then
    echo ""
    echo "🔐 Creating SSL directory..."
    mkdir -p ssl
    
    # Generate self-signed certificate for testing
    echo "Generating self-signed certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=lunaverse" 2>/dev/null || true
fi

# Stop existing services if running
echo ""
echo "🛑 Stopping existing services (if any)..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod down 2>/dev/null || true

# Build and start services
echo ""
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for services
echo ""
echo "⏳ Waiting for services to start..."
sleep 20

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.prod.yml ps

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || {
    echo -e "${YELLOW}⚠️  Migrations may have failed - will retry...${NC}"
    sleep 10
    docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
}

# Seed demo data (optional)
echo ""
read -p "Seed demo data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌱 Seeding demo data..."
    docker-compose -f docker-compose.prod.yml exec -T backend python scripts/seed_demo_data.py || {
        echo -e "${YELLOW}⚠️  Demo data seeding failed - check logs${NC}"
    }
fi

# Health checks
echo ""
echo "🏥 Running health checks..."
sleep 10

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    echo "Check logs: docker-compose -f docker-compose.prod.yml logs backend"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is healthy${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
    echo "Check logs: docker-compose -f docker-compose.prod.yml logs frontend"
fi

# Final summary
echo ""
echo "=========================================================="
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
