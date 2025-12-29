# Production Deployment Guide

This guide covers deploying the Bitcoin Estate Planning Platform to production using Docker.

## 🎯 Quick Decision Guide

**Not sure which deployment option to choose?** See [DEPLOYMENT_DECISION.md](../../docs/DEPLOYMENT_DECISION.md) for a detailed comparison.

**Recommended: Start with Lunaverse Server** (free, your existing server)
- See: [LUNAVERSE_DEPLOYMENT.md](../../docs/LUNAVERSE_DEPLOYMENT.md) for step-by-step guide
- Use: `scripts/deploy-to-lunaverse.sh` for automated deployment

**Alternative: DigitalOcean App Platform** (managed, ~$42/month)
- See: [DigitalOcean App Platform](#digitalocean-app-platform) section below

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured (optional but recommended)
- SSL certificates (for HTTPS)
- Environment variables configured

## Quick Start

1. **Copy environment file**
   ```bash
   cd infra/docker
   cp .env.prod.example .env.prod
   ```

2. **Edit `.env.prod`** with your production values:
   - Generate `SECRET_KEY`: `openssl rand -base64 32`
   - Generate `NEXTAUTH_SECRET`: `openssl rand -base64 32`
   - Set `POSTGRES_PASSWORD` to a strong password
   - Update `CORS_ORIGINS` with your domain
   - Update `NEXT_PUBLIC_API_URL` and `NEXTAUTH_URL` with your domain

3. **Set up SSL certificates** (Let's Encrypt recommended)
   ```bash
   # Place certificates in infra/docker/ssl/
   # cert.pem and key.pem
   ```

4. **Update nginx.conf** to enable HTTPS (uncomment SSL sections)

5. **Build and start services**
   ```bash
   docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
   ```

6. **Run database migrations**
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
   ```

## Deployment Platforms

### DigitalOcean App Platform

1. Connect your GitHub repository
2. Configure build settings:
   - **Backend**: Dockerfile at `backend/Dockerfile`
   - **Frontend**: Dockerfile at `frontend/client-portal/Dockerfile`
3. Set environment variables
4. Configure database (PostgreSQL managed database)
5. Configure Redis (managed Redis)
6. Set up custom domain and SSL

### Railway

1. Create new project
2. Add PostgreSQL database
3. Add Redis
4. Deploy backend from `backend/` directory
5. Deploy frontend from `frontend/client-portal/` directory
6. Configure environment variables
7. Set up custom domain

### AWS (ECS/Fargate)

1. Build and push Docker images to ECR
2. Create ECS cluster
3. Create task definitions for backend and frontend
4. Set up RDS PostgreSQL database
5. Set up ElastiCache Redis
6. Configure Application Load Balancer with SSL
7. Set up Route53 for domain

### Self-Hosted VPS

1. SSH into your VPS
2. Install Docker and Docker Compose
3. Clone repository
4. Follow Quick Start steps above
5. Set up reverse proxy (nginx) with SSL
6. Configure firewall rules

## Environment Variables

### Required Variables

- `POSTGRES_PASSWORD` - Database password
- `SECRET_KEY` - Backend secret key
- `NEXTAUTH_SECRET` - Frontend auth secret
- `NEXTAUTH_URL` - Frontend URL
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `CORS_ORIGINS` - Allowed CORS origins

### Optional Variables

- `BITCOIN_NETWORK` - mainnet or testnet (default: testnet)
- `POSTGRES_DB` - Database name (default: bitcoin_estate)
- `POSTGRES_USER` - Database user (default: postgres)

## Database Migrations

Run migrations after deployment:

```bash
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## Monitoring

### Health Checks

- Backend: `http://yourdomain.com/health`
- Frontend: `http://yourdomain.com/`

### Logs

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

## Backup

### Database Backup

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres bitcoin_estate > backup.sql

# Restore backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres bitcoin_estate < backup.sql
```

## Updates

1. Pull latest code
2. Rebuild images: `docker-compose -f docker-compose.prod.yml build`
3. Restart services: `docker-compose -f docker-compose.prod.yml up -d`
4. Run migrations if needed: `docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head`

## Troubleshooting

### Services won't start

- Check logs: `docker-compose -f docker-compose.prod.yml logs`
- Verify environment variables are set correctly
- Check database connectivity

### Database connection errors

- Verify `DATABASE_URL` is correct
- Check PostgreSQL is running and healthy
- Verify network connectivity between services

### Frontend can't connect to backend

- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS configuration
- Verify backend is running and healthy

## Security Checklist

- [ ] Strong passwords for all services
- [ ] SSL/TLS certificates configured
- [ ] Environment variables secured (not in git)
- [ ] Database backups configured
- [ ] Rate limiting enabled (nginx)
- [ ] Firewall rules configured
- [ ] Regular security updates
- [ ] Monitoring and alerting set up

