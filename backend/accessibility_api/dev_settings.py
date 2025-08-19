"""
Development settings for accessibility_api.

This file imports the base settings so the DJANGO_SETTINGS_MODULE
`accessibility_api.dev_settings` exposes the same attributes (like
ROOT_URLCONF) that Django expects. Overrides for local development
can be placed here.
"""

from .settings import *  # noqa: F401,F403 - import all base settings

# Development overrides
DEBUG = True

# Allow local hosts for development convenience
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Enable CORS for local frontend while in DEBUG
CORS_ALLOW_ALL_ORIGINS = True
