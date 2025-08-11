import os

import django


def pytest_configure():
    """Configure Django settings for pytest"""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "accessibility_api.test_settings"
    )
    django.setup()
