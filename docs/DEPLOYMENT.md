# 🚀 Production Deployment Guide

## Prerequisites

1. **Digital Ocean Droplet** (recommended: 2GB RAM, 1 vCPU minimum)
2. **Domain name** pointed to your droplet's IP
3. **SSH access** to your server

## Phase 1: Server Setup

### 1. Initial Server Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login to apply docker group changes
exit
```

### 2. Clone and Setup Repository

```bash
# Clone your repository
git clone https://github.com/your-username/accessRating.info_backend.git
cd accessRating.info_backend

# Create production environment file
cp .env.prod.example .env.prod
nano .env.prod  # Edit with your actual values
```

### 3. Configure Environment Variables

Edit `.env.prod` with your actual values:

```bash
# Generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Use this output for SECRET_KEY in .env.prod
```

**Critical Environment Variables:**

- `SECRET_KEY`: Use the generated key above
- `ALLOWED_HOSTS`: Your domain and www.your-domain.com
- `DB_PASSWORD`: Strong database password
- `CORS_ALLOWED_ORIGINS`: Your frontend domain(s)
- Email settings for password resets

## Phase 2: Domain Setup

### 1. Configure Your Domain

```bash
# Update Caddyfile with your domain
./scripts/setup-ssl.sh yourdomain.com
```

Caddy will automatically:

- Obtain SSL certificates from Let's Encrypt
- Handle certificate renewal
- Configure HTTPS redirects

## Phase 3: Deployment

### 1. Deploy Application

```bash
./scripts/deploy.sh
```

### 2. Create Superuser

```bash
make prod-shell
# In Django shell:
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@yourdomain.com', 'secure-password')
exit()
```

### 3. Verify Deployment

Check these URLs:

- `https://yourdomain.com/health/` - Health check
- `https://yourdomain.com/admin/` - Admin panel
- `https://yourdomain.com/api/v1/` - API endpoints

## Phase 4: Monitoring and Maintenance

### 1. Set up Log Monitoring

```bash
# View logs
make prod-logs

# Set up log rotation (recommended)
sudo nano /etc/logrotate.d/docker
```

### 2. Database Backups

```bash
# Create backup script
nano backup-db.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U accessibility_user accessibility_db_prod > backup_${DATE}.sql
```

### 3. Security Hardening

```bash
# Set up UFW firewall
sudo ufw allow 22  # SSH
sudo ufw allow 80  # HTTP
sudo ufw allow 443 # HTTPS
sudo ufw --force enable

# Set up fail2ban (optional but recommended)
sudo apt install fail2ban -y
```

## Phase 5: Frontend Integration

### CORS Configuration

Your frontend needs to make requests to:

- API: `https://yourdomain.com/api/v1/`
- Authentication: `https://yourdomain.com/api/v1/auth/`

### HTMX Integration

For HTMX fragments, create endpoints that return HTML:

```python
# In your views.py
from django.shortcuts import render

def business_card_fragment(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    return render(request, 'businesses/business_card.html', {'business': business})
```

## 🔧 Common Issues and Solutions

### 1. Docker Build Fails

```bash
# Clear Docker cache
docker system prune -a
docker-compose -f docker-compose.prod.yml build --no-cache
```

### 2. Database Connection Issues

```bash
# Check database logs
docker-compose -f docker-compose.prod.yml logs db

# Restart database
docker-compose -f docker-compose.prod.yml restart db
```

### 3. SSL Certificate Issues

```bash
# Check Caddy logs for SSL issues
docker-compose -f docker-compose.prod.yml logs caddy

# Restart Caddy to retry certificate
docker-compose -f docker-compose.prod.yml restart caddy
```

### 4. Static Files Not Loading

```bash
# Recollect static files
make prod-collectstatic
```

## 📊 Performance Optimization

### 1. Database Optimization

- Set up connection pooling
- Configure PostgreSQL for production
- Regular VACUUM and ANALYZE

### 2. Caching Strategy

- Redis for session storage
- API response caching
- Static file caching via Caddy

### 3. Monitoring

- Set up Sentry for error tracking
- Monitor resource usage
- Set up uptime monitoring

## 🚨 Critical Security Checklist

- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` (50+ characters)
- [ ] Database password is secure
- [ ] SSL certificate is valid (Caddy handles this)
- [ ] Firewall is configured
- [ ] Admin URL is changed from `/admin/`
- [ ] CORS origins are restricted
- [ ] Environment variables are secured
- [ ] Regular security updates

## 📝 Maintenance Tasks

### Weekly

- Check logs for errors
- Monitor disk space usage
- Review access logs

### Monthly

- Update dependencies
- Security audit
- Database backup cleanup
- SSL certificate status (auto-renewed by Caddy)

### As Needed

- Scale resources based on usage
- Update Django and dependencies
- Security patches

## 🆘 Emergency Procedures

### Rollback Deployment

```bash
git checkout previous-working-commit
./scripts/deploy.sh
```

### Database Recovery

```bash
# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U accessibility_user accessibility_db_prod < backup_YYYYMMDD_HHMMSS.sql
```

### Service Health Check

```bash
curl -f https://yourdomain.com/health/ || echo "Service is down!"
```

---

**Remember**: Always test changes in a staging environment first!
