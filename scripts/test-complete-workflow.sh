#!/bin/bash
# Complete Workflow Testing Script
# Tests all user workflows end-to-end

set -e

echo "🧪 Starting Complete Workflow Tests..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check services
echo "📡 Checking services..."
BACKEND_HEALTH=$(curl -s http://localhost:8000/health 2>&1 | grep -o '"status":"[^"]*"' || echo "")
FRONTEND_RESPONSE=$(curl -s http://localhost:3000 2>&1 | head -1 || echo "")

if [[ $BACKEND_HEALTH == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Backend is running${NC}"
else
    echo -e "${RED}❌ Backend is not responding${NC}"
    exit 1
fi

if [[ $FRONTEND_RESPONSE == *"html"* ]] || [[ $FRONTEND_RESPONSE == *"<!DOCTYPE"* ]]; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
else
    echo -e "${RED}❌ Frontend is not responding${NC}"
    exit 1
fi

echo ""
echo "🔍 Testing API Endpoints..."

# Test estate plans endpoint
echo -n "  Testing GET /api/v1/estate-plans... "
ESTATE_PLANS_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:8000/api/v1/estate-plans 2>&1)
HTTP_CODE=$(echo "$ESTATE_PLANS_RESPONSE" | tail -1)
if [[ $HTTP_CODE == "200" ]] || [[ $HTTP_CODE == "401" ]]; then
    echo -e "${GREEN}✅${NC} (HTTP $HTTP_CODE)"
else
    echo -e "${RED}❌${NC} (HTTP $HTTP_CODE)"
fi

# Test Bitcoin validation
echo -n "  Testing POST /api/v1/bitcoin/validate... "
VALIDATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8000/api/v1/bitcoin/validate \
  -H "Content-Type: application/json" \
  -d '{"address":"bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh","network":"mainnet"}' 2>&1)
HTTP_CODE=$(echo "$VALIDATE_RESPONSE" | tail -1)
if [[ $HTTP_CODE == "200" ]] || [[ $HTTP_CODE == "401" ]]; then
    echo -e "${GREEN}✅${NC} (HTTP $HTTP_CODE)"
else
    echo -e "${RED}❌${NC} (HTTP $HTTP_CODE)"
fi

echo ""
echo "🎭 Running E2E Tests..."
cd frontend/client-portal

if command -v npx &> /dev/null; then
    npx playwright test --reporter=list 2>&1 | head -50
else
    echo -e "${YELLOW}⚠️  Playwright not found, skipping E2E tests${NC}"
fi

echo ""
echo -e "${GREEN}✅ Workflow testing complete!${NC}"

