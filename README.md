# AccessRating.info Backend

A production-ready Django REST API backend for the AccessRating.info platform, providing accessibility ratings and business information services.

## 🏗️ Architecture

- **Backend**: Django 5.2.4 with Django REST Framework
- **Database**: PostgreSQL with connection pooling
- **Cache**: Redis for session and query caching
- **Reverse Proxy**: Caddy with automatic HTTPS/SSL
- **Containerization**: Docker with multi-stage builds
- **Security**: Production hardened with security headers, CORS, and environment isolation

## 📁 Project Structure

```
accessRating.info_backend/
├── backend/                    # Django application code
│   ├── accessibility_api/      # Django project settings
│   ├── apps/                   # Django applications
│   ├── requirements.txt        # Development dependencies
│   ├── requirements-prod.txt   # Production dependencies
│   └── manage.py              # Django management script
├── docker/                     # Container configurations
│   ├── Dockerfile             # Production container build
│   ├── docker-compose.prod.yml # Production orchestration
│   └── .dockerignore          # Docker ignore rules
├── caddy/                      # Reverse proxy configuration
│   └── Caddyfile              # Caddy server config
├── scripts/                    # Deployment and utility scripts
│   ├── deploy.sh              # Production deployment
│   └── setup-ssl.sh           # SSL certificate setup
├── docs/                       # Documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── SECURITY.md            # Security documentation
│   ├── QUICKSTART.md          # Quick start guide
│   └── PRODUCTION_CHECKLIST.md # Production readiness checklist
├── .env.prod.example          # Production environment template
├── .gitignore                 # Git ignore rules
├── Makefile                   # Development and production commands
└── README.md                  # This file
```

## 🚀 Quick Start

### Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/pixel-87/accessRating.info_backend.git
   cd accessRating.info_backend
   ```

2. **Set up virtual environment:**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   make install
   ```

4. **Start development database:**

   ```bash
   make db-up
   ```

5. **Run migrations:**

   ```bash
   make migrate
   ```

6. **Start development server:**
   ```bash
   make run
   ```

### Production Deployment

1. **Prepare environment:**

   ```bash
   cp .env.prod.example .env.prod
   # Edit .env.prod with your production values
   ```

2. **Configure domain (if you have one):**

   ```bash
   ./scripts/setup-ssl.sh your-domain.com
   ```

3. **Deploy:**
   ```bash
   make deploy
   ```

## 🛠️ Available Commands

### Development

- `make install` - Install development dependencies
- `make test` - Run test suite
- `make run` - Start development server
- `make migrate` - Run database migrations
- `make shell` - Open Django shell

### Production

- `make deploy` - Deploy to production
- `make prod-up` - Start production services
- `make prod-down` - Stop production services
- `make prod-logs` - View production logs
- `make prod-migrate` - Run production migrations

## 🔒 Security Features

- HTTPS enforcement with automatic SSL certificates
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Secure session and cookie settings
- Environment variable protection
- Non-root Docker containers
- CORS configuration for frontend integration
- Database connection encryption

## 📚 Documentation

- [**Deployment Guide**](docs/DEPLOYMENT.md) - Complete deployment instructions
- [**Security Guide**](docs/SECURITY.md) - Security configuration and best practices
- [**Quick Start Guide**](docs/QUICKSTART.md) - Getting started quickly
- [**Production Checklist**](docs/PRODUCTION_CHECKLIST.md) - Pre-deployment verification

## 🏥 Health Monitoring

The application includes a health check endpoint at `/health/` that monitors:

- Database connectivity
- Cache (Redis) connectivity
- Application status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Support

For support and questions:

- Create an issue in this repository
- Check the documentation in the `docs/` folder
- Review the production checklist for deployment issues

- `backend/` – Django API
- `docs/` – Documentation
- `docker-compose.yml` – PostgreSQL setup

## Quick Start

Clone repo, set up Python & Docker, run migrations, start server:

```
git clone <repo-url>
cd accessRatingScheme/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
python manage.py migrate
python manage.py runserver
```

## API Endpoints

- `GET /api/v1/businesses/` – List businesses
- `POST /api/v1/businesses/` – Create business
- `GET /api/v1/businesses/{id}/` – Business details

## Status

- Backend: Stable, tested
- Frontend: Static site (separate repo)
- Deployment: VPS/Docker

## Contributing

- Follow Django best practices
- Write tests
- Update docs

## License

[Add license]
