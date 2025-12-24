#!/bin/bash

# Bitcoin Estate Planning Platform - Start All Services
# This script starts all required services for the application

set -e

PROJECT_ROOT="/Users/Javad/Starter_Pack/bitcoin-estate-planning"
cd "$PROJECT_ROOT"

echo "🚀 Starting Bitcoin Estate Planning Platform..."
echo ""

# Check if .env files exist
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env not found"
    echo "   Copy backend/env.example to backend/.env and configure it"
    echo ""
fi

if [ ! -f "frontend/client-portal/.env.local" ]; then
    echo "⚠️  Warning: frontend/client-portal/.env.local not found"
    echo "   Copy frontend/client-portal/env.example to frontend/client-portal/.env.local and configure it"
    echo ""
fi

# Start Docker services
echo "📦 Starting Docker services (PostgreSQL, Redis)..."
docker-compose -f infra/docker/docker-compose.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 3

# Check if services are running
if docker-compose -f infra/docker/docker-compose.yml ps | grep -q "Up"; then
    echo "✅ Docker services started"
else
    echo "❌ Docker services failed to start"
    exit 1
fi

echo ""
echo "✅ All services started!"
echo ""
echo "📋 Next steps:"
echo "  1. Start backend (Terminal 2):"
echo "     cd $PROJECT_ROOT/backend"
echo "     source .venv/bin/activate"
echo "     uvicorn app.main:app --reload"
echo ""
echo "  2. Start frontend (Terminal 3):"
echo "     cd $PROJECT_ROOT/frontend/client-portal"
echo "     npm run dev"
echo ""
echo "  3. Open browser: http://localhost:3000"
echo ""

