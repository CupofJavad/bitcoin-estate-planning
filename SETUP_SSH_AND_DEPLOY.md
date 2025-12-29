# One-Time SSH Setup for Automated Deployments

## Quick Setup (5 minutes)

### Step 1: Add Your SSH Key to Server

**On your MacBook, run:**

```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub
```

**Then SSH to your server and run:**

```bash
ssh luna@100.80.191.90
# Enter your password when prompted

# Once connected, run:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# Paste your public key (from the cat command above)
# Press Ctrl+X, then Y, then Enter to save

chmod 600 ~/.ssh/authorized_keys
exit
```

### Step 2: Test Passwordless SSH

**Back on your MacBook:**

```bash
ssh luna@100.80.191.90 "echo '✅ Passwordless SSH works!'"
```

If this works without asking for a password, you're all set!

### Step 3: Deploy Automatically

**Now you can deploy with one command:**

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
bash scripts/deploy-lunaverse-direct.sh
```

This script will:
- ✅ Connect to server automatically
- ✅ Pull latest code from GitHub
- ✅ Build all Docker containers
- ✅ Run database migrations
- ✅ Seed demo data
- ✅ Check service health
- ✅ Report any errors

## Alternative: Manual Deployment

If you prefer to deploy manually on the server:

```bash
# SSH to server
ssh luna@100.80.191.90

# Run these commands:
cd ~/bitcoin-estate-planning
git pull origin feature/v2-core-enhancements
cd infra/docker
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait for build (5-10 minutes)
# Then check status:
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

## Troubleshooting

### SSH Key Not Working

1. **Check key permissions on server:**
   ```bash
   ssh luna@100.80.191.90
   ls -la ~/.ssh/
   # Should show: authorized_keys with 600 permissions
   ```

2. **Check server SSH config:**
   ```bash
   ssh luna@100.80.191.90
   sudo nano /etc/ssh/sshd_config
   # Ensure these are set:
   # PubkeyAuthentication yes
   # AuthorizedKeysFile .ssh/authorized_keys
   # Then restart: sudo systemctl restart sshd
   ```

### Deployment Fails

1. **Check Docker is running:**
   ```bash
   ssh luna@100.80.191.90 "docker ps"
   ```

2. **Check logs:**
   ```bash
   ssh luna@100.80.191.90 "cd ~/bitcoin-estate-planning/infra/docker && docker-compose -f docker-compose.prod.yml logs"
   ```

3. **Rebuild from scratch:**
   ```bash
   ssh luna@100.80.191.90 "cd ~/bitcoin-estate-planning/infra/docker && docker-compose -f docker-compose.prod.yml down && docker-compose -f docker-compose.prod.yml up -d --build"
   ```

---

**Once SSH is set up, all future deployments can be automated!** 🚀

