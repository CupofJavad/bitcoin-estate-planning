#!/bin/bash
# GitHub Repository Setup Script
# Run this script to create and push to GitHub

set -e

REPO_NAME="bitcoin-estate-planning"
GITHUB_USER="CupofJavad"
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "🚀 Setting up GitHub repository..."
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI found"
    echo "Creating repository with GitHub CLI..."
    gh repo create ${REPO_NAME} \
        --public \
        --description "Bitcoin-native estate planning platform with timelock policies, beneficiary management, and automated inheritance workflows" \
        --source=. \
        --remote=origin \
        --push
    echo "✓ Repository created and pushed!"
else
    echo "GitHub CLI not found. Please create the repository manually:"
    echo ""
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: ${REPO_NAME}"
    echo "3. Description: Bitcoin-native estate planning platform with timelock policies, beneficiary management, and automated inheritance workflows"
    echo "4. Set to Public"
    echo "5. DO NOT initialize with README, .gitignore, or license (we already have these)"
    echo "6. Click 'Create repository'"
    echo ""
    echo "Then run these commands:"
    echo "  git remote add origin ${REPO_URL}"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    echo ""
    read -p "Press Enter after you've created the repository on GitHub..."
    
    # Add remote and push
    git remote add origin ${REPO_URL} 2>/dev/null || git remote set-url origin ${REPO_URL}
    git branch -M main
    git push -u origin main
    echo "✓ Code pushed to GitHub!"
fi

echo ""
echo "✅ Repository is now live at: https://github.com/${GITHUB_USER}/${REPO_NAME}"

