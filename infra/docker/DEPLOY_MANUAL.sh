#!/bin/bash
# Manual deployment script for Lunaverse
# Run this on your Lunaverse server after setting up .env.prod

set -e

echo "🚀 Bitcoin Estate Planning - Manual Deployment"
echo "=============================================="
echo ""

# Check if .env.prod exists
if [ ! -f ".env.prod" ]; then
    echo "❌ .env.prod file not found!"
    echo "Please create .env.prod from .env.prod.template first"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 15

# Run migrations
echo "🗄️  Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || {
    echo "⚠️  Migrations may have failed - check logs"
}

# Health checks
echo "🏥 Checking service health..."
sleep 5

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
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "📝 Next steps:"
echo "  - Check logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  - Access frontend: http://100.80.191.90:3000"
echo "  - Access backend: http://100.80.191.90:8000/docs"

