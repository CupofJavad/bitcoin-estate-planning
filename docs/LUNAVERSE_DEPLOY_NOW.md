# Deploy to Lunaverse - Right Now! 🚀

## You're Already Connected - Let's Deploy!

### Step 1: Create .env.prod File

```bash
# On Lunaverse server (you're already there)
cd ~/bitcoin-estate-planning/infra/docker

# Copy the template
cp .env.prod.template .env.prod

# Edit with your values
nano .env.prod
```

### Step 2: Update .env.prod with Your Values

**Replace these placeholders in .env.prod:**

1. **POSTGRES_PASSWORD**: Generate a strong password
   ```bash
   openssl rand -base64 24
   ```

2. **POSTGRES_SUPERUSER_PASSWORD**: Generate another strong password
   ```bash
   openssl rand -base64 24
   ```

3. **SECRET_KEY**: Generate for backend
   ```bash
   openssl rand -base64 32
   ```

4. **NEXTAUTH_SECRET**: Generate for frontend
   ```bash
   openssl rand -base64 32
   ```

5. **LUNAVERSE_SSH_PASSWORD**: Use your actual SSH password from your secrets file

6. **OPENAI_API_KEY**: (Optional) Add if you want chatbot to work

7. **DEFAULT_ADMIN_PASSWORD**: Choose a secure admin password

**Example .env.prod (with your format):**
```bash
# Copy from your secrets file and adapt:
# - POSTGRES_USER=postgres (keep as is)
# - POSTGRES_PASSWORD="<generated>"
# - SECRET_KEY="<generated>"
# - NEXTAUTH_SECRET="<generated>"
# - LUNAVERSE_SSH_PASSWORD="Lunatic_2025*!" (from your secrets)
```

### Step 3: Create SSL Directory (for HTTPS)

```bash
# Create SSL directory
mkdir -p ssl

# Generate self-signed certificate (for testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=lunaverse"
```

### Step 4: Make Deployment Script Executable

```bash
cd ~/bitcoin-estate-planning/infra/docker
chmod +x DEPLOY_MANUAL.sh
```

### Step 5: Run Deployment

```bash
# Run the deployment script
./DEPLOY_MANUAL.sh
```

### Alternative: Manual Commands (if script doesn't work)

```bash
# Build and start
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Wait a moment
sleep 15

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Check status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 6: Configure Firewall (if needed)

```bash
# Allow necessary ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 8000/tcp
sudo ufw enable
```

### Step 7: Access Your Application

**From your MacBook:**
- Frontend: `http://100.80.191.90:3000`
- Backend API Docs: `http://100.80.191.90:8000/docs`
- Backend Health: `http://100.80.191.90:8000/health`

---

## Quick Reference Commands

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Stop services
docker-compose -f docker-compose.prod.yml down

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

---

## Troubleshooting

### Permission Denied
```bash
# Make sure you're in docker group
newgrp docker
# Or log out and back in
```

### Services Won't Start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check disk space
df -h

# Check memory
free -h
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose -f docker-compose.prod.yml ps postgres

# Check database logs
docker-compose -f docker-compose.prod.yml logs postgres
```

---

**You're ready to deploy! Follow the steps above.** 🚀

