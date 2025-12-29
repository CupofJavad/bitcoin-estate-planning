#!/bin/bash

# DigitalOcean App Platform Deployment Script
# This script helps prepare and deploy to DigitalOcean App Platform

set -e

echo "🚀 DigitalOcean App Platform Deployment Helper"
echo "=============================================="
echo ""

# Check if .do/app.yaml exists
if [ ! -f ".do/app.yaml" ]; then
    echo "❌ Error: .do/app.yaml not found!"
    echo "   Please ensure you're in the project root directory."
    exit 1
fi

echo "✅ Found .do/app.yaml configuration"
echo ""

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo "   It's recommended to commit all changes before deploying"
    read -p "   Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📦 Current branch: $CURRENT_BRANCH"
echo ""

# Check if branch is pushed
if [ -z "$(git log origin/$CURRENT_BRANCH..HEAD 2>/dev/null)" ]; then
    echo "✅ Branch is up to date with remote"
else
    echo "⚠️  Warning: Local branch has unpushed commits"
    read -p "   Push to GitHub now? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin "$CURRENT_BRANCH"
        echo "✅ Pushed to GitHub"
    fi
fi

echo ""
echo "📋 Deployment Checklist:"
echo "   1. ✅ Code is in GitHub"
echo "   2. ✅ .do/app.yaml configuration exists"
echo ""
echo "🔧 Next Steps:"
echo ""
echo "   1. Go to DigitalOcean Dashboard:"
echo "      https://cloud.digitalocean.com/apps"
echo ""
echo "   2. Click 'Create App' → 'GitHub'"
echo ""
echo "   3. Select repository: CupofJavad/bitcoin-estate-planning"
echo "      Branch: $CURRENT_BRANCH"
echo ""
echo "   4. DigitalOcean will detect .do/app.yaml automatically"
echo ""
echo "   5. Configure environment variables:"
echo "      - SECRET_KEY (generate: openssl rand -base64 32)"
echo "      - NEXTAUTH_SECRET (generate: openssl rand -base64 32)"
echo "      - NEXT_PUBLIC_API_URL (your backend URL)"
echo "      - NEXTAUTH_URL (your frontend URL)"
echo "      - CORS_ORIGINS (your domains)"
echo ""
echo "   6. Review configuration and deploy"
echo ""
echo "   7. After deployment, run database migrations:"
echo "      - Go to backend service → Console"
echo "      - Run: alembic upgrade head"
echo ""
echo "📚 Full guide: docs/DIGITALOCEAN_DEPLOYMENT.md"
echo ""
echo "✨ Ready to deploy!"

