# Backend Development

## Project Structure

```
backend/
├── accessibility_api/       # Django project configuration
│   ├── settings.py         # Main settings
│   ├── test_settings.py    # Test-specific settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── apps/                   # Django applications
│   ├── accounts/          # User management
│   └── businesses/        # Business data & ratings
├── media/                 # User uploads (photos, docs)
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
└── requirements.txt      # Python dependencies
```

## Development Workflow

### Setup

```bash
# Install dependencies
make install

# Start database
make db-up

# Run migrations
make migrate

# Create superuser
make superuser
```

### Daily Development

```bash
# Run tests
make test

# Run with coverage
make test-cov

# Start development server
make run

# Format code
make format

# Run linting
make lint
```

### Database Management

```bash
# Create migrations after model changes
make makemigrations

# Apply migrations
make migrate

# Reset database (destroys all data)
make db-reset
```

## API Documentation

### Authentication Endpoints

- `POST /api/v1/auth/registration/` - Register new user
- `POST /api/v1/auth/login/` - Login user
- `POST /api/v1/auth/logout/` - Logout user
- `GET /api/v1/auth/user/` - Get current user details

### Business Endpoints

- `GET /api/v1/businesses/` - List businesses (with filtering)
- `POST /api/v1/businesses/` - Create new business
- `GET /api/v1/businesses/{id}/` - Get business details
- `PUT/PATCH /api/v1/businesses/{id}/` - Update business
- `DELETE /api/v1/businesses/{id}/` - Delete business

### Query Parameters

- `?accessibility_level=3` - Filter by accessibility level
- `?business_type=cafe` - Filter by business type
- `?search=coffee` - Search by name/description
- `?owner=me` - Show only user's businesses

## Testing

- **57 total tests** covering all components
- **Models**: Business logic and validation
- **Serializers**: API data transformation
- **Views**: HTTP endpoints and permissions
- **URLs**: Route resolution

Run tests with: `make test`

## Database Schema

### User & Profiles

- `User` (Django built-in) - Basic authentication
- `UserProfile` - Extended user information
- `BusinessOwner` - Business ownership verification
- `AccessibilityExpert` - Professional assessor credentials

### Business Data

- `Business` - Core business information & accessibility rating
- `BusinessReview` - User reviews and feedback
- `BusinessPhoto` - Business photos and accessibility features

## Environment Variables

Required in `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=accessibility_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```
