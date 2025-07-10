"""
Global pytest configuration for the accessibility_api project.
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def pytest_configure():
    """Configure Django settings for pytest."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accessibility_api.test_settings')
    django.setup()


def pytest_runtest_setup(item):
    """Set up each test."""
    pass


def pytest_runtest_teardown(item, nextitem):
    """Tear down each test."""
    pass
