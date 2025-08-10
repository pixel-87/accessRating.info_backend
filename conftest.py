import os
import sys


def pytest_configure():
    """Configure pytest for Django in the backend directory"""
    # Add the backend directory to the Python path
    backend_path = os.path.join(os.path.dirname(__file__), "backend")
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    # Set Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accessibility_api.test_settings")

    # Import and setup Django
    import django

    django.setup()


def pytest_collection_modifyitems(config, items):
    """Modify test collection to only include tests from backend directory"""
    backend_tests = []
    for item in items:
        if "backend/" in str(item.fspath) or "/backend" in str(item.fspath):
            backend_tests.append(item)
    items[:] = backend_tests
