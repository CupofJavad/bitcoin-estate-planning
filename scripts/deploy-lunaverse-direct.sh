#!/bin/bash
# Direct deployment script - runs commands on server via SSH
# Requires SSH key authentication (run setup-ssh-key.sh first)

set -e

LUNAVERSE_HOST="100.80.191.90"
LUNAVERSE_USER="luna"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🚀 Bitcoin Estate Planning - Direct Lunaverse Deployment"
echo "========================================================"
echo ""

# Test SSH connection
echo "🔌 Testing SSH connection..."
if ! ssh -o BatchMode=yes -o ConnectTimeout=5 "$LUNAVERSE_USER@$LUNAVERSE_HOST" "echo 'Connected'" > /dev/null 2>&1; then
    echo -e "${RED}❌ SSH connection failed${NC}"
    echo ""
    echo "Please run: bash scripts/setup-ssh-key.sh"
    echo "This will set up passwordless SSH authentication."
    exit 1
fi

echo -e "${GREEN}✅ SSH connection successful${NC}"
echo ""

# Deploy script to run on server
DEPLOY_SCRIPT=$(cat << 'DEPLOYEOF'
#!/bin/bash
set -e

cd ~/bitcoin-estate-planning || {
    echo "📥 Cloning repository..."
    cd ~
    git clone https://github.com/CupofJavad/bitcoin-estate-planning.git
    cd bitcoin-estate-planning
    git checkout feature/v2-core-enhancements
}

echo "📥 Updating repository..."
git fetch origin
git checkout feature/v2-core-enhancements
git pull origin feature/v2-core-enhancements

cd infra/docker

# Create .env.prod if needed
if [ ! -f ".env.prod" ]; then
    echo "📝 Creating .env.prod..."
    POSTGRES_PASS=$(openssl rand -base64 24)
    SECRET_KEY=$(openssl rand -base64 32)
    NEXTAUTH_SECRET=$(openssl rand -base64 32)
    cat > .env.prod << EOF
POSTGRES_DB=bitcoin_estate
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${POSTGRES_PASS}
SECRET_KEY=${SECRET_KEY}
BITCOIN_NETWORK=testnet
CORS_ORIGINS=http://100.80.191.90,http://100.80.191.90:3000,http://localhost:3000
NEXT_PUBLIC_API_URL=http://100.80.191.90:8000/api
NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
NEXTAUTH_URL=http://100.80.191.90
REDIS_URL=redis://redis:6379/0
EOF
fi

# Create SSL if needed
mkdir -p ssl
if [ ! -f "ssl/cert.pem" ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/CN=lunaverse" 2>/dev/null || true
fi

# Stop existing
docker-compose -f docker-compose.prod.yml --env-file .env.prod down 2>/dev/null || true

# Build and start
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for services
echo "⏳ Waiting for services..."
sleep 30

# Run migrations
echo "🗄️  Running migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || {
    sleep 10
    docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
}

# Seed data
echo "🌱 Seeding demo data..."
docker-compose -f docker-compose.prod.yml exec -T backend python scripts/seed_demo_data.py || true

# Status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.prod.yml ps

# Health checks
echo ""
echo "🏥 Health Checks:"
curl -f http://localhost:8000/health > /dev/null 2>&1 && echo "✅ Backend healthy" || echo "❌ Backend failed"
curl -f http://localhost:3000 > /dev/null 2>&1 && echo "✅ Frontend healthy" || echo "❌ Frontend failed"

echo ""
echo "✅ Deployment complete!"
echo "🌐 Access: http://100.80.191.90:3000"
DEPLOYEOF
)

# Execute on server
echo "📤 Deploying to server..."
ssh "$LUNAVERSE_USER@$LUNAVERSE_HOST" "bash -s" <<< "$DEPLOY_SCRIPT"

echo ""
echo -e "${GREEN}✅ Deployment completed!${NC}"

