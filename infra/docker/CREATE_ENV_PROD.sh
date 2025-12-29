#!/bin/bash
# Script to create .env.prod file with your secret format
# Run this on Lunaverse server

cat > .env.prod << 'ENVEOF'
# =========================================
# Bitcoin Estate Planning - Production Environment
# =========================================

# =========================================
# App / Environment
# =========================================
APP_ENV=production
LOG_LEVEL=INFO

# =========================================
# Lunaverse Server (SSH + endpoints)
# =========================================
SERVER_ADMIN_NAME="Luna Server Admin"
SERVER_NAME=lunaverse

LUNAVERSE_HOST=192.168.1.172
LUNAVERSE_SSH_USER=luna
LUNAVERSE_SSH_PORT=22
LUNAVERSE_SSH_PASSWORD="REPLACE_WITH_YOUR_SSH_PASSWORD"
LUNAVERSE_SSH_TAILSCALE_HOST=100.80.191.90

COCKPIT_URL="https://192.168.1.172:9090"
PGADMIN_URL="http://192.168.1.172:5050/browser/"

# =========================================
# PostgreSQL (Docker Container - Production)
# =========================================
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=bitcoin_estate

POSTGRES_USER=postgres
POSTGRES_PASSWORD="REPLACE_WITH_STRONG_PASSWORD"

POSTGRES_SUPERUSER=postgres
POSTGRES_SUPERUSER_PASSWORD="REPLACE_WITH_STRONG_PASSWORD"

# =========================================
# Backend Configuration (FastAPI)
# =========================================
SECRET_KEY="REPLACE_WITH_GENERATED_SECRET_KEY"
BITCOIN_NETWORK=testnet
CORS_ORIGINS=http://100.80.191.90,https://100.80.191.90,http://localhost:3000

# =========================================
# Frontend Configuration (Next.js)
# =========================================
NEXT_PUBLIC_API_URL=http://100.80.191.90:8000/api
NEXTAUTH_SECRET="REPLACE_WITH_GENERATED_SECRET_KEY"
NEXTAUTH_URL=http://100.80.191.90

# =========================================
# Redis Configuration (Docker Container)
# =========================================
REDIS_URL=redis://redis:6379/0

# =========================================
# OpenAI (for Chatbot - Optional)
# =========================================
OPENAI_API_KEY="REPLACE_WITH_YOUR_OPENAI_API_KEY"

# =========================================
# App seeded admin user (from seed script)
# =========================================
DEFAULT_ADMIN_EMAIL=admin@example.com
DEFAULT_ADMIN_PASSWORD="REPLACE_WITH_ADMIN_PASSWORD"
DEFAULT_ADMIN_ROLE=admin

# =========================================
# GitHub (for CI/CD - Optional)
# =========================================
GITHUB_TOKEN="REPLACE_WITH_YOUR_GITHUB_TOKEN"
ENVEOF

echo "✅ Created .env.prod file"
echo ""
echo "📝 Next steps:"
echo "  1. Edit .env.prod: nano .env.prod"
echo "  2. Replace all REPLACE_WITH_* placeholders"
echo "  3. Generate passwords:"
echo "     - POSTGRES_PASSWORD: openssl rand -base64 24"
echo "     - SECRET_KEY: openssl rand -base64 32"
echo "     - NEXTAUTH_SECRET: openssl rand -base64 32"

