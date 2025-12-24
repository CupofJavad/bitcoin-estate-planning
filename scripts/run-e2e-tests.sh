#!/bin/bash
# Run E2E tests with proper setup

set -e

cd "$(dirname "$0")/.."

echo "🧪 Running E2E Tests..."
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
  echo "⚠️  Backend is not running on port 8000"
  echo "   Please start the backend first:"
  echo "   cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
  echo ""
  read -p "Continue anyway? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Check if frontend is running
if ! curl -s http://localhost:3004 > /dev/null 2>&1 && ! curl -s http://localhost:3000 > /dev/null 2>&1; then
  echo "⚠️  Frontend is not running"
  echo "   Tests will start the frontend automatically"
  echo ""
fi

# Run tests
cd frontend/client-portal

echo "📦 Installing Playwright browsers (if needed)..."
npx playwright install chromium --with-deps || true

echo ""
echo "🚀 Running E2E tests..."
echo ""

# Set environment variables
export FRONTEND_URL=${FRONTEND_URL:-http://localhost:3004}
export API_URL=${API_URL:-http://localhost:8000}

npm run test:e2e

echo ""
echo "✅ Tests completed!"
echo ""
echo "📊 View test report:"
echo "   npm run test:e2e:report"
echo ""

