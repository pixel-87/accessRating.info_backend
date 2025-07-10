"""
URL patterns for the businesses app.
"""
from rest_framework.routers import DefaultRouter

from . import views

# Create a router for the ViewSet
router = DefaultRouter()
router.register(r'', views.BusinessViewSet)

# URL patterns
urlpatterns = router.urls
