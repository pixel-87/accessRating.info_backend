from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessViewSet, BusinessPhotoViewSet, BusinessReviewViewSet

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet)
router.register(r'business-photos', BusinessPhotoViewSet)
router.register(r'business-reviews', BusinessReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]