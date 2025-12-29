#!/bin/bash
# Deployment script for Lunaverse server
# Usage: ./deploy-to-lunaverse.sh

set -e  # Exit on error

echo "🚀 Bitcoin Estate Planning - Lunaverse Deployment Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on server
if [ -z "$SSH_CONNECTION" ] && [ -z "$LUNAVERSE_HOST" ]; then
    echo -e "${YELLOW}⚠️  This script should be run on your Lunaverse server${NC}"
    echo "Or set LUNAVERSE_HOST environment variable for remote deployment"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Docker
echo "📦 Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please install Docker first:"
    echo "  sudo apt-get update && sudo apt-get install -y docker.io docker-compose"
    exit 1
fi
echo -e "${GREEN}✅ Docker is installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose is installed${NC}"

# Check if we're in the right directory
if [ ! -f "infra/docker/docker-compose.prod.yml" ]; then
    echo -e "${RED}❌ docker-compose.prod.yml not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Navigate to docker directory
cd infra/docker

# Check for .env.prod file
if [ ! -f ".env.prod" ]; then
    echo -e "${YELLOW}⚠️  .env.prod file not found${NC}"
    echo "Creating .env.prod from template..."
    
    # Generate secure passwords
    SECRET_KEY=$(openssl rand -base64 32)
    NEXTAUTH_SECRET=$(openssl rand -base64 32)
    POSTGRES_PASSWORD=$(openssl rand -base64 24)
    
    cat > .env.prod << EOF
# Database Configuration
POSTGRES_DB=bitcoin_estate
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

# Backend Configuration
SECRET_KEY=${SECRET_KEY}
BITCOIN_NETWORK=testnet
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
NEXTAUTH_URL=http://localhost:3000
EOF
    
    echo -e "${GREEN}✅ Created .env.prod${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env.prod and update:${NC}"
    echo "  - CORS_ORIGINS with your domain"
    echo "  - NEXT_PUBLIC_API_URL with your domain"
    echo "  - NEXTAUTH_URL with your domain"
    echo ""
    read -p "Press Enter to continue after editing .env.prod..."
fi

# Check SSL certificates
if [ ! -d "ssl" ] || [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
    echo -e "${YELLOW}⚠️  SSL certificates not found${NC}"
    echo "Options:"
    echo "  1. Use Let's Encrypt (recommended for production)"
    echo "  2. Generate self-signed certificate (for testing)"
    echo "  3. Skip SSL setup (HTTP only)"
    read -p "Choose option (1/2/3): " ssl_option
    
    case $ssl_option in
        1)
            echo "Please set up Let's Encrypt certificates manually:"
            echo "  sudo certbot certonly --standalone -d yourdomain.com"
            echo "Then copy certificates to infra/docker/ssl/"
            read -p "Press Enter after setting up SSL certificates..."
            ;;
        2)
            echo "Generating self-signed certificate..."
            mkdir -p ssl
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout ssl/key.pem \
                -out ssl/cert.pem \
                -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
            echo -e "${GREEN}✅ Self-signed certificate created${NC}"
            ;;
        3)
            echo -e "${YELLOW}⚠️  Skipping SSL setup - will use HTTP only${NC}"
            ;;
    esac
fi

# Build and start services
echo ""
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.prod.yml ps

# Run database migrations
echo ""
echo "🗄️  Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || {
    echo -e "${YELLOW}⚠️  Migrations may have failed - check logs${NC}"
}

# Health checks
echo ""
echo "🏥 Running health checks..."
sleep 5

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is healthy${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
fi

# Final instructions
echo ""
echo "=================================================="
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📝 Next steps:"
echo "  1. Check logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  2. Access frontend: http://your-server-ip or https://yourdomain.com"
echo "  3. Access backend API: http://your-server-ip:8000/docs"
echo "  4. Set up backups (see docs/LUNAVERSE_DEPLOYMENT.md)"
echo "  5. Configure firewall (allow ports 80 and 443)"
echo ""
echo "📚 Documentation:"
echo "  - Full guide: docs/LUNAVERSE_DEPLOYMENT.md"
echo "  - Troubleshooting: docs/LUNAVERSE_DEPLOYMENT.md#troubleshooting"
echo ""

