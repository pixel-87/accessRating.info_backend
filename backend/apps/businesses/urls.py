from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessViewSet, BusinessPhotoViewSet, BusinessReviewViewSet, business_search_html
from .views import business_locations, business_card_html

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet)
router.register(r'business-photos', BusinessPhotoViewSet)
router.register(r'business-reviews', BusinessReviewViewSet)

urlpatterns = [
    path('search/', business_search_html, name='business_search_html'),
    path('businesses/<int:business_id>/card/', business_card_html, name='business_card_html'),
    path('', include(router.urls)),
    path('business-locations/', business_locations, name='business_locations'),
]