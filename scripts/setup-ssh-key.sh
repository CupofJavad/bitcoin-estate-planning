#!/bin/bash
# Setup SSH key for automated deployments
# Run this on your MacBook to enable passwordless SSH to Lunaverse

set -e

echo "🔐 Setting up SSH key for Lunaverse server"
echo "==========================================="
echo ""

LUNAVERSE_HOST="100.80.191.90"
LUNAVERSE_USER="luna"

# Check if SSH key exists
if [ ! -f "$HOME/.ssh/id_rsa" ] && [ ! -f "$HOME/.ssh/id_ed25519" ]; then
    echo "📝 Generating new SSH key..."
    ssh-keygen -t ed25519 -C "lunaverse-deployment" -f "$HOME/.ssh/id_ed25519" -N ""
    echo "✅ SSH key generated"
else
    echo "✅ SSH key already exists"
fi

# Determine which key to use
if [ -f "$HOME/.ssh/id_ed25519.pub" ]; then
    PUB_KEY="$HOME/.ssh/id_ed25519.pub"
elif [ -f "$HOME/.ssh/id_rsa.pub" ]; then
    PUB_KEY="$HOME/.ssh/id_rsa.pub"
else
    echo "❌ No public key found"
    exit 1
fi

echo ""
echo "📋 Your public key:"
cat "$PUB_KEY"
echo ""
echo ""
echo "📤 Copying SSH key to server..."
echo "   You'll be prompted for your password once"
echo ""

# Copy key to server
ssh-copy-id -i "$PUB_KEY" "$LUNAVERSE_USER@$LUNAVERSE_HOST" || {
    echo ""
    echo "⚠️  ssh-copy-id failed. Manual setup required:"
    echo ""
    echo "1. Copy your public key:"
    echo "   cat $PUB_KEY"
    echo ""
    echo "2. SSH to server:"
    echo "   ssh $LUNAVERSE_USER@$LUNAVERSE_HOST"
    echo ""
    echo "3. Run on server:"
    echo "   mkdir -p ~/.ssh"
    echo "   chmod 700 ~/.ssh"
    echo "   echo '$(cat $PUB_KEY)' >> ~/.ssh/authorized_keys"
    echo "   chmod 600 ~/.ssh/authorized_keys"
    echo ""
    exit 1
}

echo ""
echo "✅ SSH key copied successfully!"
echo ""
echo "🧪 Testing connection..."
ssh -o BatchMode=yes -o ConnectTimeout=5 "$LUNAVERSE_USER@$LUNAVERSE_HOST" "echo '✅ Passwordless SSH works!'" && {
    echo ""
    echo "🎉 Setup complete! You can now run deployments without passwords."
} || {
    echo ""
    echo "⚠️  Passwordless SSH test failed. You may need to:"
    echo "   1. Check server SSH configuration"
    echo "   2. Verify key permissions"
    echo "   3. Try manual key setup (see above)"
}

