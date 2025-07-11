# Access Rating Scheme

A Django-based accessibility rating platform for UK businesses.

## 🎯 Project Overview

The Access Rating Scheme is a voluntary initiative to rate businesses (1-5) based on physical accessibility, helping disabled individuals make informed decisions about business visits.

## 🏗️ Architecture

```
accessRatingScheme/
├── backend/              # Django REST API
├── docs/                # Project documentation
├── docker-compose.yml   # PostgreSQL database
└── .github/            # CI/CD workflows
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Docker & Docker Compose

### Setup

```bash
# Clone and setup
git clone <repo-url>
cd accessRatingScheme

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Database setup
docker-compose up -d  # Start PostgreSQL
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Testing

```bash
cd backend
python -m pytest  # Run all tests (57 tests)
python -m pytest --cov  # With coverage report
```

## 📋 API Endpoints

- `POST /api/v1/auth/registration/` - User registration
- `POST /api/v1/auth/login/` - User login
- `GET /api/v1/businesses/` - List businesses
- `POST /api/v1/businesses/` - Create business
- `GET /api/v1/businesses/{id}/` - Get business details

## 🧪 Current Status

- ✅ **Backend**: Django REST API with comprehensive tests (57/57 passing)
- ✅ **Authentication**: JWT-based auth with user roles
- ✅ **Business Management**: Full CRUD operations
- ✅ **Google Maps Integration**: Location coordinates ready
- 🚧 **Frontend**: React app (planned)
- 🚧 **Deployment**: Production setup (planned)

## 📚 Documentation

See `/docs/` folder for:

- `MVP_Development_Plan.md` - Complete development roadmap and phases
- `AccessratingOverview.md` - Business requirements and objectives
- `requirements.md` - Technical specifications

## 🤝 Contributing

1. Follow Django best practices
2. Write tests for new features
3. Update documentation
4. Use conventional commit messages

## 📄 License

[Add your license here]
