#!/bin/bash

# Bitcoin Estate Planning Platform - Environment Setup Script
# This script helps set up environment files with generated secrets

set -e

PROJECT_ROOT="/Users/Javad/Starter_Pack/bitcoin-estate-planning"
cd "$PROJECT_ROOT"

echo "🔧 Setting up environment files..."
echo ""

# Generate secrets
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
NEXTAUTH_SECRET=$(openssl rand -base64 32)

# Backend .env
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env..."
    cp backend/env.example backend/.env
    
    # Replace SECRET_KEY
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|SECRET_KEY=your-secret-key-change-in-production|SECRET_KEY=$SECRET_KEY|" backend/.env
    else
        # Linux
        sed -i "s|SECRET_KEY=your-secret-key-change-in-production|SECRET_KEY=$SECRET_KEY|" backend/.env
    fi
    
    echo "✅ Backend .env created with generated SECRET_KEY"
else
    echo "ℹ️  backend/.env already exists, skipping..."
fi

# Frontend .env.local
if [ ! -f "frontend/client-portal/.env.local" ]; then
    echo "📝 Creating frontend/client-portal/.env.local..."
    cp frontend/client-portal/env.example frontend/client-portal/.env.local
    
    # Add NEXTAUTH_SECRET and NEXTAUTH_URL
    echo "" >> frontend/client-portal/.env.local
    echo "NEXTAUTH_SECRET=$NEXTAUTH_SECRET" >> frontend/client-portal/.env.local
    echo "NEXTAUTH_URL=http://localhost:3000" >> frontend/client-portal/.env.local
    
    echo "✅ Frontend .env.local created with generated NEXTAUTH_SECRET"
else
    echo "ℹ️  frontend/client-portal/.env.local already exists, skipping..."
fi

echo ""
echo "✅ Environment setup complete!"
echo ""
echo "📋 Generated secrets:"
echo "   Backend SECRET_KEY: Generated"
echo "   Frontend NEXTAUTH_SECRET: Generated"
echo ""
echo "⚠️  Important: Keep these secrets secure and never commit them to git!"
echo ""

