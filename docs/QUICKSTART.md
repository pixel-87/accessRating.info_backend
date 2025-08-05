# 🚀 Quick Production Setup Guide

## CRITICAL: Before You Start

Your Django backend is now configured for production with:

1. **Secure settings** - Production Django configuration
2. **Caddy reverse proxy** - Automatic HTTPS and security headers
3. **PostgreSQL** - Production database with connection pooling
4. **Redis cache** - Session storage and caching
5. **Health monitoring** - `/health/` endpoint for monitoring
6. **Docker deployment** - Containerized for consistency

## 30-Minute Production Deployment

### Step 1: Prepare Your Server (5 min)

```bash
# On your Digital Ocean droplet
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
sudo usermod -aG docker $USER
exit  # Logout and login again
```

### Step 2: Clone and Configure (10 min)

```bash
git clone https://github.com/your-username/accessRating.info_backend.git
cd accessRating.info_backend

# Configure environment
cp .env.prod.example .env.prod
nano .env.prod  # EDIT THIS WITH YOUR VALUES

# Generate secure secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Update Domain (2 min)

```bash
# Replace 'your-domain.com' with your actual domain in Caddyfile
./scripts/setup-ssl.sh yourdomain.com
```

### Step 4: Deploy (10 min)

```bash
# Deploy application (Caddy handles SSL automatically)
./scripts/deploy.sh

# Create admin user
make prod-shell
# In Django shell:
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@yourdomain.com', 'secure-password')
exit()
```

### Step 5: Verify (3 min)

Visit these URLs to verify everything works:

- `https://yourdomain.com/health/` ✅
- `https://yourdomain.com/admin/` ✅
- `https://yourdomain.com/api/v1/` ✅

## CRITICAL: Required Environment Variables

In your `.env.prod` file, you MUST set:

```bash
SECRET_KEY=your-50-character-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=accessibility_db_prod
DB_USER=accessibility_user
DB_PASSWORD=super-secure-password-here
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

## Common Deployment Issues

### Issue: "SECRET_KEY is required"

**Solution**: Generate a proper secret key using the Python command above

### Issue: "ALLOWED_HOSTS not configured"

**Solution**: Set your actual domain in ALLOWED_HOSTS

### Issue: SSL certificate fails

**Solution**: Check that your domain DNS points to your server IP. Caddy will automatically retry SSL certificate generation.

### Issue: Database connection fails

**Solution**: Check DB_PASSWORD and DB_USER in .env.prod

## Production vs Development Differences

| Feature      | Development      | Production         |
| ------------ | ---------------- | ------------------ |
| DEBUG        | True             | False              |
| CORS         | Allow all        | Specific domains   |
| Database     | Local PostgreSQL | Managed PostgreSQL |
| Static Files | Django serves    | Caddy + WhiteNoise |
| SSL          | Not required     | Required           |
| Caching      | No cache         | Redis cache        |
| Logging      | Console only     | File + Console     |

## Next Steps After Deployment

1. **Set up monitoring** - Monitor your /health/ endpoint
2. **Configure backups** - Database backups are critical
3. **Set up DNS** - Configure your domain properly
4. **Test everything** - Create test data, test all endpoints
5. **Connect frontend** - Update your frontend to use the new API URLs

## Get Help

If you run into issues:

1. Check logs: `make prod-logs`
2. Verify environment: Check `.env.prod` values
3. Test health check: `curl https://yourdomain.com/health/`
4. Check SSL: `openssl s_client -connect yourdomain.com:443`

---

**Remember**: Test everything before going live with real users!
