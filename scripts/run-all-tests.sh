#!/bin/bash
# Complete Test Suite Runner
# Runs all tests and provides comprehensive results

set -e

echo "🧪 Bitcoin Estate Planning - Complete Test Suite"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check services
echo -e "${BLUE}📡 Checking Services...${NC}"
BACKEND_HEALTH=$(curl -s http://localhost:8000/health 2>&1 | grep -o '"status":"[^"]*"' || echo "")
FRONTEND_CHECK=$(curl -s http://localhost:3000 2>&1 | head -1 || echo "")

if [[ $BACKEND_HEALTH == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Backend: Running${NC}"
else
    echo -e "${RED}❌ Backend: Not responding${NC}"
    exit 1
fi

if [[ $FRONTEND_CHECK == *"html"* ]] || [[ $FRONTEND_CHECK == *"<!DOCTYPE"* ]]; then
    echo -e "${GREEN}✅ Frontend: Running${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend: May not be running${NC}"
fi

echo ""
echo -e "${BLUE}🔍 Testing API Endpoints...${NC}"

# Test estate plans
ESTATE_PLANS=$(curl -s -w "\n%{http_code}" http://localhost:8000/api/v1/estate-plans 2>&1)
HTTP_CODE=$(echo "$ESTATE_PLANS" | tail -1)
if [[ $HTTP_CODE == "200" ]]; then
    echo -e "${GREEN}✅ GET /api/v1/estate-plans: OK${NC}"
    COUNT=$(echo "$ESTATE_PLANS" | head -1 | python3 -c "import sys, json; data=sys.stdin.read(); d=json.loads(data) if data.strip() else []; print(len(d) if isinstance(d, list) else 0)" 2>/dev/null || echo "0")
    echo "   Found $COUNT estate plans"
else
    echo -e "${RED}❌ GET /api/v1/estate-plans: HTTP $HTTP_CODE${NC}"
fi

# Test Bitcoin validation
VALIDATE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8000/api/v1/bitcoin/validate \
  -H "Content-Type: application/json" \
  -d '{"address":"bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh","network":"mainnet"}' 2>&1)
HTTP_CODE=$(echo "$VALIDATE" | tail -1)
if [[ $HTTP_CODE == "200" ]]; then
    echo -e "${GREEN}✅ POST /api/v1/bitcoin/validate: OK${NC}"
else
    echo -e "${RED}❌ POST /api/v1/bitcoin/validate: HTTP $HTTP_CODE${NC}"
fi

echo ""
echo -e "${BLUE}🎭 Running E2E Tests...${NC}"
cd frontend/client-portal

if command -v npx &> /dev/null; then
    npx playwright test --reporter=list --workers=1 --project=chromium 2>&1 | tee /tmp/e2e-results.log
    EXIT_CODE=${PIPESTATUS[0]}
    
    if [[ $EXIT_CODE == 0 ]]; then
        echo -e "${GREEN}✅ All E2E tests passed!${NC}"
    else
        echo -e "${YELLOW}⚠️  Some E2E tests failed. Check /tmp/e2e-results.log for details${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Playwright not found, skipping E2E tests${NC}"
fi

echo ""
echo -e "${BLUE}📊 Test Summary${NC}"
echo "=================="
echo "Check test results above for detailed information"
echo ""
echo -e "${GREEN}✅ Test suite execution complete!${NC}"

