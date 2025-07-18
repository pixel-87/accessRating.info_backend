from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessViewSet, BusinessPhotoViewSet, BusinessReviewViewSet, business_search_html

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet)
router.register(r'business-photos', BusinessPhotoViewSet)
router.register(r'business-reviews', BusinessReviewViewSet)

urlpatterns = [
    path('search/', business_search_html, name='business_search_html'),
    path('', include(router.urls)),
]