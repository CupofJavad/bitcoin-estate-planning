# Deploy to Lunaverse - Quick Start

## 🚀 Easiest Method: Run on Server

### Step 1: SSH to Your Server

```bash
ssh luna@100.80.191.90
```

### Step 2: Install Docker (if not installed)

```bash
# Check if Docker is installed
docker --version

# If not installed, run:
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker

# Verify you can run docker without sudo
docker ps
```

### Step 3: Download and Run Deployment Script

```bash
# Download the deployment script
curl -o deploy.sh https://raw.githubusercontent.com/CupofJavad/bitcoin-estate-planning/feature/v2-core-enhancements/scripts/deploy-lunaverse-interactive.sh

# Make it executable
chmod +x deploy.sh

# Run it
bash deploy.sh
```

**OR** if you already have the repo cloned:

```bash
cd ~/bitcoin-estate-planning
git pull origin feature/v2-core-enhancements
bash scripts/deploy-lunaverse-interactive.sh
```

## ✅ That's It!

The script will:
- ✅ Clone/update the repository
- ✅ Generate secure passwords
- ✅ Create environment file
- ✅ Build and start all services
- ✅ Run database migrations
- ✅ Seed demo data
- ✅ Verify everything is working

## 🌐 Access Your App

After deployment:
- **Frontend:** http://100.80.191.90:3000
- **Backend:** http://100.80.191.90:8000
- **API Docs:** http://100.80.191.90:8000/docs

## 🔑 Demo User

- **Email:** demo@example.com
- **Password:** demo123456

## 🆘 Troubleshooting

### Docker Permission Denied

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Services Won't Start

```bash
cd ~/bitcoin-estate-planning/infra/docker
docker-compose -f docker-compose.prod.yml logs
```

### Port Already in Use

```bash
# Check what's using the port
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000

# Stop conflicting services or change ports in docker-compose.prod.yml
```

---

**Ready to deploy!** Just SSH and run the script! 🚀

