# DigitalOcean App Platform Deployment Guide

Complete guide for deploying Bitcoin Estate Planning Platform to DigitalOcean App Platform.

## 🎯 Overview

DigitalOcean App Platform is a fully managed platform that handles:
- Automatic deployments from GitHub
- SSL certificates
- Auto-scaling
- Health checks
- Database management
- Monitoring and logs

**Estimated Monthly Cost:** ~$42/month
- Backend: $5/month (Basic XXS)
- Frontend: $5/month (Basic XXS)
- PostgreSQL: $15/month (Basic)
- Redis: $15/month (Basic)

## 📋 Prerequisites

1. **DigitalOcean Account**
   - Sign up at https://www.digitalocean.com
   - Add payment method

2. **GitHub Repository**
   - Code must be in GitHub (already done ✅)
   - Repository: `CupofJavad/bitcoin-estate-planning`
   - Branch: `feature/v2-core-enhancements`

3. **Domain Name** (Optional but recommended)
   - Configure DNS records
   - Point to DigitalOcean

## 🚀 Quick Deployment Steps

### Step 1: Create App in DigitalOcean

1. **Log in to DigitalOcean**
   - Go to https://cloud.digitalocean.com
   - Navigate to **Apps** → **Create App**

2. **Connect GitHub Repository**
   - Click **GitHub** tab
   - Authorize DigitalOcean to access your GitHub
   - Select repository: `CupofJavad/bitcoin-estate-planning`
   - Select branch: `feature/v2-core-enhancements`

3. **Configure App**
   - DigitalOcean will detect the `.do/app.yaml` file
   - Review the configuration
   - Click **Edit** if you need to adjust settings

### Step 2: Configure Environment Variables

In the DigitalOcean dashboard, add these environment variables:

#### Required Variables

```bash
# Backend Service
SECRET_KEY=<generate-strong-secret-key>
BITCOIN_NETWORK=testnet
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Frontend Service
NEXT_PUBLIC_API_URL=https://your-backend-url.ondigitalocean.app
NEXTAUTH_URL=https://your-frontend-url.ondigitalocean.app
NEXTAUTH_SECRET=<generate-strong-secret-key>
```

#### Generate Secrets

```bash
# Generate SECRET_KEY
openssl rand -base64 32

# Generate NEXTAUTH_SECRET
openssl rand -base64 32
```

### Step 3: Configure Databases

1. **PostgreSQL Database**
   - DigitalOcean will create a managed PostgreSQL database
   - Note the connection string (auto-injected as `DATABASE_URL`)
   - Database name: `bitcoin_estate`
   - User: `bitcoin_app`

2. **Redis Database**
   - DigitalOcean will create a managed Redis instance
   - Connection URL auto-injected as `REDIS_URL`

### Step 4: Review and Deploy

1. **Review Configuration**
   - Check all services are configured
   - Verify environment variables
   - Review resource allocations

2. **Deploy**
   - Click **Create Resources**
   - DigitalOcean will:
     - Build Docker images
     - Deploy services
     - Set up databases
     - Configure networking
     - Set up SSL certificates

3. **Wait for Deployment**
   - Initial deployment takes 5-10 minutes
   - Monitor progress in the dashboard
   - Check logs if issues occur

### Step 5: Run Database Migrations

After deployment, run database migrations:

1. **Access Backend Console**
   - Go to your app in DigitalOcean
   - Click on **backend** service
   - Open **Console** tab

2. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

3. **Seed Demo Data** (Optional)
   ```bash
   python scripts/seed_demo_data.py
   ```

### Step 6: Configure Custom Domain (Optional)

1. **Add Domain**
   - Go to **Settings** → **Domains**
   - Click **Add Domain**
   - Enter your domain name

2. **Update DNS**
   - Add CNAME record pointing to your app
   - DigitalOcean will provide the target

3. **SSL Certificate**
   - DigitalOcean automatically provisions SSL
   - Wait for certificate to be issued (5-10 minutes)

4. **Update Environment Variables**
   - Update `NEXT_PUBLIC_API_URL` with your domain
   - Update `NEXTAUTH_URL` with your domain
   - Update `CORS_ORIGINS` with your domain
   - Redeploy services

## 🔧 Configuration Details

### Backend Service

- **Instance Size:** Basic XXS (512MB RAM, 1 vCPU)
- **Port:** 8000
- **Health Check:** `/health`
- **Workers:** 2 (configured in Dockerfile)

### Frontend Service

- **Instance Size:** Basic XXS (512MB RAM, 1 vCPU)
- **Port:** 3000
- **Health Check:** `/`
- **Build:** Standalone Next.js build

### Database Configuration

- **PostgreSQL:** Version 15
- **Database Name:** `bitcoin_estate`
- **User:** `bitcoin_app`
- **Connection:** Auto-injected via `DATABASE_URL`

- **Redis:** Version 7
- **Connection:** Auto-injected via `REDIS_URL`

## 📊 Monitoring

### Health Checks

- Backend: `https://your-backend-url.ondigitalocean.app/health`
- Frontend: `https://your-frontend-url.ondigitalocean.app/`

### Logs

Access logs in DigitalOcean dashboard:
- Go to your app
- Click on service (backend/frontend)
- View **Runtime Logs** tab

### Metrics

DigitalOcean provides:
- Request rates
- Response times
- Error rates
- Resource usage (CPU, Memory)

## 🔄 Updates and Deployments

### Automatic Deployments

- Pushes to `feature/v2-core-enhancements` branch trigger automatic deployments
- DigitalOcean builds and deploys new versions
- Zero-downtime deployments

### Manual Deployments

1. Go to your app in DigitalOcean
2. Click **Actions** → **Create Deployment**
3. Select branch/commit
4. Click **Create Deployment**

### Rollback

If deployment fails:
1. Go to **Deployments** tab
2. Find previous successful deployment
3. Click **Rollback**

## 🔐 Security

### Environment Variables

- Mark sensitive variables as **SECRET** in DigitalOcean
- Secrets are encrypted at rest
- Never commit secrets to git

### SSL/TLS

- DigitalOcean automatically provisions SSL certificates
- Certificates auto-renew
- HTTPS enforced by default

### Database Security

- Managed databases are in private networks
- Only accessible from your app
- Automatic backups enabled
- Point-in-time recovery available

## 💰 Cost Optimization

### Current Setup
- **Total:** ~$42/month
- Backend: $5/month
- Frontend: $5/month
- PostgreSQL: $15/month
- Redis: $15/month

### Scaling Options

**If traffic increases:**
- Upgrade instance sizes
- Add more instances (horizontal scaling)
- Enable auto-scaling

**If cost is a concern:**
- Start with smaller instance sizes
- Use shared databases (if available)
- Monitor usage and optimize

## 🆘 Troubleshooting

### Deployment Fails

1. **Check Build Logs**
   - Go to **Deployments** tab
   - Click on failed deployment
   - Review build logs

2. **Common Issues**
   - Dockerfile errors
   - Missing environment variables
   - Database connection issues
   - Build timeout

### Services Won't Start

1. **Check Runtime Logs**
   - View service logs in dashboard
   - Look for error messages

2. **Common Issues**
   - Missing environment variables
   - Database connection errors
   - Port conflicts
   - Health check failures

### Database Connection Issues

1. **Verify Connection String**
   - Check `DATABASE_URL` is set correctly
   - Ensure database is running
   - Verify network connectivity

2. **Test Connection**
   - Use backend console
   - Run: `python -c "from app.core.database import engine; print('Connected')"`

### Frontend Can't Connect to Backend

1. **Check Environment Variables**
   - Verify `NEXT_PUBLIC_API_URL` is correct
   - Check CORS configuration
   - Ensure backend is accessible

2. **Test API**
   - Visit backend health endpoint
   - Check CORS headers
   - Verify network connectivity

## 📝 Post-Deployment Checklist

- [ ] All services are running
- [ ] Health checks passing
- [ ] Database migrations completed
- [ ] Demo data seeded (if needed)
- [ ] Custom domain configured (if using)
- [ ] SSL certificates active
- [ ] Environment variables set correctly
- [ ] Monitoring configured
- [ ] Backups enabled
- [ ] Documentation updated

## 🔗 Useful Links

- [DigitalOcean App Platform Docs](https://docs.digitalocean.com/products/app-platform/)
- [App Spec Reference](https://docs.digitalocean.com/products/app-platform/reference/app-spec/)
- [Managed Databases](https://docs.digitalocean.com/products/databases/)

## 📞 Support

If you encounter issues:
1. Check DigitalOcean status page
2. Review application logs
3. Check DigitalOcean community forums
4. Contact DigitalOcean support

---

**Last Updated:** December 29, 2024

