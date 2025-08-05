# 🔒 Django Production Security Checklist

## Critical Security Settings

### ✅ Environment Configuration

- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` (50+ characters, unique)
- [ ] `ALLOWED_HOSTS` restricted to your domains only
- [ ] Database credentials are secure and unique
- [ ] `.env.prod` file has proper permissions (600)

### ✅ HTTPS and SSL

- [ ] SSL certificate installed and valid
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] HSTS headers configured (`SECURE_HSTS_SECONDS`)
- [ ] Mixed content blocked
- [ ] Certificate auto-renewal working

### ✅ Database Security

- [ ] Database user has minimal required permissions
- [ ] Database password is strong (12+ chars, mixed)
- [ ] Database connection uses SSL (`sslmode=require`)
- [ ] Connection pooling configured
- [ ] Regular backups scheduled

### ✅ Authentication & Sessions

- [ ] Strong password requirements enforced
- [ ] Session cookies secure (`SESSION_COOKIE_SECURE = True`)
- [ ] CSRF protection enabled
- [ ] JWT tokens have reasonable expiry times
- [ ] Admin interface URL changed from `/admin/`

### ✅ CORS and Headers

- [ ] CORS origins restricted to your frontend domains
- [ ] Security headers configured:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`

### ✅ File Handling

- [ ] Media files served securely (not through Django)
- [ ] File upload size limits configured
- [ ] File type validation implemented
- [ ] Static files served with proper caching headers

### ✅ Infrastructure Security

- [ ] Firewall configured (ports 22, 80, 443 only)
- [ ] SSH key authentication (password auth disabled)
- [ ] Regular system updates scheduled
- [ ] Fail2ban configured for SSH protection
- [ ] Docker images use non-root users

### ✅ Monitoring and Logging

- [ ] Error tracking (Sentry) configured
- [ ] Access logs monitored
- [ ] Health checks implemented
- [ ] Disk space monitoring
- [ ] Resource usage alerts

### ✅ Data Protection

- [ ] Database backups automated and tested
- [ ] Sensitive data encrypted at rest
- [ ] Personal data handling complies with GDPR
- [ ] Data retention policies defined

## Django Security Commands

```bash
# Check for security issues
python manage.py check --deploy

# Test with security settings
python manage.py diffsettings --output=unified

# Check for common vulnerabilities
pip install safety
safety check
```

## Regular Security Tasks

### Daily

- [ ] Monitor error logs
- [ ] Check failed login attempts

### Weekly

- [ ] Review access logs
- [ ] Check SSL certificate status
- [ ] Monitor resource usage

### Monthly

- [ ] Update dependencies
- [ ] Security audit
- [ ] Backup verification
- [ ] Review user permissions

### Quarterly

- [ ] Penetration testing
- [ ] Security policy review
- [ ] Incident response testing
- [ ] Staff security training

---

**Never ignore security warnings in production!**
