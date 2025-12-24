#!/bin/bash
# Restart backend server to apply CORS changes

set -e

cd "$(dirname "$0")/.."

echo "🔄 Restarting Backend Server..."
echo ""

# Find and kill existing backend process
PID=$(lsof -ti:8000 2>/dev/null | head -1)
if [ -n "$PID" ]; then
  echo "⚠️  Found existing backend process (PID: $PID)"
  echo "   Killing process..."
  kill $PID
  sleep 2
  
  # Check if it's still running
  if lsof -ti:8000 >/dev/null 2>&1; then
    echo "   Force killing..."
    kill -9 $PID
    sleep 1
  fi
  echo "✅ Process killed"
else
  echo "ℹ️  No existing backend process found"
fi

echo ""
echo "🚀 Starting backend server..."
echo ""

cd backend

# Activate virtual environment
if [ ! -d ".venv" ]; then
  echo "❌ Virtual environment not found. Run 'make setup-backend' first."
  exit 1
fi

source .venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
  echo "⚠️  .env file not found. Creating from env.example..."
  if [ -f "env.example" ]; then
    cp env.example .env
    echo "✅ Created .env from env.example"
    echo "⚠️  Please update .env with your configuration"
  else
    echo "❌ env.example not found"
    exit 1
  fi
fi

# Start backend
echo "📡 Starting uvicorn on http://localhost:8000"
echo ""
uvicorn app.main:app --reload

