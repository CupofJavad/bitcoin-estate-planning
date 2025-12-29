# Lunaverse Server Deployment Guide

## Resource Requirements Assessment

### Application Requirements

**Minimum Resources Needed:**
- **CPU**: 2 cores (can work with 1, but 2 recommended)
- **RAM**: 2GB minimum (4GB recommended for comfortable operation)
- **Disk**: 10GB minimum (20GB recommended for database growth)
- **Network**: Standard internet connection

**Service Breakdown:**
- **Backend (FastAPI)**: ~200-300MB RAM, minimal CPU
- **Frontend (Next.js)**: ~100-200MB RAM, minimal CPU
- **PostgreSQL**: ~300-500MB RAM, minimal CPU
- **Redis**: ~50-100MB RAM, minimal CPU
- **Nginx**: ~20-50MB RAM, minimal CPU

**Total Estimated Usage:**
- **Minimum**: ~1GB RAM, 1 CPU core
- **Recommended**: ~2GB RAM, 2 CPU cores
- **Comfortable**: ~4GB RAM, 2-4 CPU cores

### Can Lunaverse Support This?

**✅ YES - Lunaverse can easily support this application!**

**Why:**
1. **Lightweight Stack**: All services are containerized and optimized
2. **Efficient Resources**: Docker containers share resources efficiently
3. **Low Traffic Expected**: Estate planning app won't have high concurrent users initially
4. **Scalable**: Can add resources later if needed

**Recommendation: Start with Lunaverse, monitor, and scale if needed.**

---

## Pre-Deployment Checklist

### Server Requirements

- [ ] **Docker installed** (version 20.10+)
- [ ] **Docker Compose installed** (version 2.0+)
- [ ] **At least 2GB free RAM**
- [ ] **At least 10GB free disk space**
- [ ] **Ports 80 and 443 available** (for Nginx)
- [ ] **SSH access** to the server
- [ ] **Domain name** (optional, but recommended for SSL)

### Access Requirements

- [ ] **SSH access** configured
- [ ] **Tailscale** configured (if using Tailscale for access)
- [ ] **Firewall** configured to allow ports 80, 443, and SSH

---

## Step-by-Step Deployment

### Step 1: Connect to Lunaverse Server

**Via Tailscale (Recommended):**
```bash
ssh -p ${LUNAVERSE_SSH_PORT:-22} ${LUNAVERSE_SSH_USER}@${LUNAVERSE_SSH_TAILSCALE_HOST}
```

**Via Direct IP:**
```bash
ssh -p ${LUNAVERSE_SSH_PORT:-22} ${LUNAVERSE_SSH_USER}@${LUNAVERSE_HOST}
```

### Step 2: Install Docker and Docker Compose

**On Ubuntu/Debian:**
```bash
# Update package index
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io docker-compose

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
# Or run: newgrp docker

# Verify installation
docker --version
docker-compose --version
```

**On other Linux distributions:**
- Follow Docker's official installation guide for your distribution

### Step 3: Clone Repository on Server

```bash
# Navigate to your preferred directory
cd /opt  # or /home/youruser, or wherever you prefer

# Clone the repository
git clone https://github.com/yourusername/bitcoin-estate-planning.git
cd bitcoin-estate-planning
```

**Or transfer files via SCP:**
```bash
# From your MacBook
scp -r bitcoin-estate-planning ${LUNAVERSE_SSH_USER}@${LUNAVERSE_SSH_TAILSCALE_HOST}:/opt/
```

### Step 4: Create Production Environment File

```bash
cd /opt/bitcoin-estate-planning/infra/docker

# Create .env.prod file
cat > .env.prod << 'EOF'
# Database Configuration
POSTGRES_DB=bitcoin_estate
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<GENERATE_STRONG_PASSWORD>

# Backend Configuration
SECRET_KEY=<GENERATE_SECRET_KEY>
BITCOIN_NETWORK=testnet
CORS_ORIGINS=https://yourdomain.com,http://yourdomain.com

# Frontend Configuration
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
NEXTAUTH_SECRET=<GENERATE_SECRET_KEY>
NEXTAUTH_URL=https://yourdomain.com
EOF
```

**Generate secure passwords:**
```bash
# Generate SECRET_KEY
openssl rand -base64 32

# Generate NEXTAUTH_SECRET
openssl rand -base64 32

# Generate POSTGRES_PASSWORD
openssl rand -base64 24
```

**Edit `.env.prod` and replace placeholders:**
```bash
nano .env.prod
# Or use vim, emacs, etc.
```

### Step 5: Set Up SSL Certificates (Optional but Recommended)

**Option A: Let's Encrypt (Free, Recommended)**
```bash
# Install certbot
sudo apt-get install -y certbot

# Generate certificate (replace with your domain)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to project directory
sudo mkdir -p /opt/bitcoin-estate-planning/infra/docker/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/bitcoin-estate-planning/infra/docker/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/bitcoin-estate-planning/infra/docker/ssl/key.pem
sudo chmod 644 /opt/bitcoin-estate-planning/infra/docker/ssl/*.pem
```

**Option B: Self-Signed Certificate (For Testing)**
```bash
mkdir -p /opt/bitcoin-estate-planning/infra/docker/ssl
cd /opt/bitcoin-estate-planning/infra/docker/ssl

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout key.pem \
  -out cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=yourdomain.com"
```

### Step 6: Configure Nginx

**Edit nginx.conf:**
```bash
cd /opt/bitcoin-estate-planning/infra/docker
nano nginx.conf
```

**Update the server_name and SSL paths if using SSL:**
- Replace `yourdomain.com` with your actual domain
- Update SSL certificate paths if needed

### Step 7: Build and Start Services

```bash
cd /opt/bitcoin-estate-planning/infra/docker

# Build and start all services
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 8: Run Database Migrations

```bash
cd /opt/bitcoin-estate-planning/infra/docker

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Step 9: Verify Deployment

**Check services:**
```bash
# Check all containers are running
docker-compose -f docker-compose.prod.yml ps

# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000
```

**Access the application:**
- **With domain**: `https://yourdomain.com`
- **Without domain**: `http://your-server-ip` (if ports are exposed)

---

## Post-Deployment Configuration

### Set Up Automatic Backups

**Create backup script:**
```bash
cat > /opt/bitcoin-estate-planning/scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/bitcoin-estate"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
docker-compose -f /opt/bitcoin-estate-planning/infra/docker/docker-compose.prod.yml \
  exec -T postgres pg_dump -U postgres bitcoin_estate > $BACKUP_DIR/db_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
EOF

chmod +x /opt/bitcoin-estate-planning/scripts/backup.sh
```

**Set up cron job (daily backups at 2 AM):**
```bash
crontab -e
# Add this line:
0 2 * * * /opt/bitcoin-estate-planning/scripts/backup.sh
```

### Set Up Monitoring (Optional)

**Monitor resource usage:**
```bash
# Install monitoring tools
sudo apt-get install -y htop iotop

# View container stats
docker stats
```

### Set Up Log Rotation

**Configure Docker log rotation:**
```bash
sudo nano /etc/docker/daemon.json
```

**Add:**
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

**Restart Docker:**
```bash
sudo systemctl restart docker
```

---

## Maintenance Commands

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Restart Services
```bash
# Restart all
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend
```

### Update Application
```bash
cd /opt/bitcoin-estate-planning

# Pull latest code
git pull

# Rebuild and restart
cd infra/docker
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations if needed
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Stop Services
```bash
docker-compose -f docker-compose.prod.yml down
```

### Start Services
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Services Won't Start

**Check logs:**
```bash
docker-compose -f docker-compose.prod.yml logs
```

**Check disk space:**
```bash
df -h
```

**Check memory:**
```bash
free -h
```

### Database Connection Issues

**Check PostgreSQL is running:**
```bash
docker-compose -f docker-compose.prod.yml ps postgres
```

**Check database logs:**
```bash
docker-compose -f docker-compose.prod.yml logs postgres
```

**Test connection:**
```bash
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d bitcoin_estate
```

### Frontend Can't Connect to Backend

**Check environment variables:**
```bash
docker-compose -f docker-compose.prod.yml exec frontend env | grep API
```

**Check backend is accessible:**
```bash
docker-compose -f docker-compose.prod.yml exec frontend curl http://backend:8000/health
```

### Port Already in Use

**Check what's using the port:**
```bash
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
```

**Stop conflicting service or change ports in docker-compose.prod.yml**

---

## Security Considerations

### Firewall Configuration

**Allow only necessary ports:**
```bash
# Install UFW if not installed
sudo apt-get install -y ufw

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### Regular Updates

**Update system packages:**
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

**Update Docker images:**
```bash
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### SSL Certificate Renewal

**If using Let's Encrypt, set up auto-renewal:**
```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot usually sets up auto-renewal automatically
# Check: sudo systemctl status certbot.timer
```

---

## Performance Optimization

### Resource Limits

**Add resource limits to docker-compose.prod.yml if needed:**
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Database Optimization

**PostgreSQL tuning (for larger datasets):**
```bash
# Edit postgresql.conf in container or use environment variables
# Consider adding to docker-compose.prod.yml:
environment:
  POSTGRES_SHARED_BUFFERS: 256MB
  POSTGRES_EFFECTIVE_CACHE_SIZE: 1GB
```

---

## When to Consider DigitalOcean

**Consider DigitalOcean if:**
- Lunaverse server has < 2GB RAM
- Lunaverse server has < 10GB disk space
- You want managed database backups
- You want automatic scaling
- You want 99.99% uptime SLA
- You prefer managed services over self-hosting

**Lunaverse is fine if:**
- ✅ Server has 2GB+ RAM
- ✅ Server has 10GB+ disk space
- ✅ You're comfortable managing the server
- ✅ You want to save on hosting costs
- ✅ You have low to moderate traffic

---

## Next Steps

1. **Test deployment** on Lunaverse
2. **Monitor resource usage** for a week
3. **Set up backups** and monitoring
4. **Configure domain** and SSL
5. **Set up CI/CD** for automated deployments

---

**Last Updated**: December 28, 2024

