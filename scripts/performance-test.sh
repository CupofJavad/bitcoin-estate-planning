#!/bin/bash
# Performance Testing Script
# Measures key performance metrics

set -e

echo "🚀 Performance Testing"
echo "======================"
echo ""

# Check if frontend is running
FRONTEND=$(curl -s http://localhost:3000 2>&1 | head -1)
if [[ $FRONTEND != *"html"* ]] && [[ $FRONTEND != *"<!DOCTYPE"* ]]; then
    echo "⚠️  Frontend not running. Start with: cd frontend/client-portal && npm run dev"
    exit 1
fi

echo "📊 Performance Metrics"
echo ""

# Measure page load time
echo "Measuring page load time..."
START=$(date +%s%N)
curl -s http://localhost:3000 > /dev/null
END=$(date +%s%N)
LOAD_TIME=$(( (END - START) / 1000000 ))
echo "  Page Load: ${LOAD_TIME}ms"

# Check bundle sizes (if build exists)
if [ -d "frontend/client-portal/.next" ]; then
    echo ""
    echo "📦 Bundle Analysis"
    echo "  Run: cd frontend/client-portal && npm run build"
    echo "  Then check .next/static for bundle sizes"
fi

echo ""
echo "💡 For detailed performance analysis:"
echo "  1. Open http://localhost:3000 in Chrome"
echo "  2. Open DevTools (F12)"
echo "  3. Go to Lighthouse tab"
echo "  4. Run Performance audit"
echo ""
echo "✅ Performance testing complete!"

