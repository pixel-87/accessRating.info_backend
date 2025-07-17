"""
Test settings for accessibility_api project.
Uses SQLite for faster test execution and overrides specific settings for testing.
"""

from datetime import timedelta
from .settings import *  # noqa: F403, F401

# Import specific settings that we'll modify
try:
    from .settings import REST_FRAMEWORK  # noqa: F401
except ImportError:
    REST_FRAMEWORK = {}

# Test database - use SQLite for speed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for faster test runs
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Faster password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}

# Test-specific Django settings
DEBUG = False
SECRET_KEY = 'test-secret-key-not-for-production'

# Allauth test settings
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

# REST Framework test settings - Use JWT for consistency with production
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    'rest_framework.authentication.TokenAuthentication',  # Fallback for legacy tests
    'rest_framework.authentication.SessionAuthentication',
]

# JWT Settings for tests - shorter expiry for faster tests
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Shorter for tests
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=1),
    'ROTATE_REFRESH_TOKENS': False,  # Disable rotation for test simplicity
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# Celery - use synchronous execution for tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
