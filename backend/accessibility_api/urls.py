"""
URL configuration for accessibility_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.businesses.urls import router as businesses_router
from apps.businesses import views as business_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),  # health and small core utilities
    path("api/v1/auth/", include("dj_rest_auth.urls")),  # Login, logout, user details
    path(
        "api/v1/auth/registration/", include("dj_rest_auth.registration.urls")
    ),  # Registration
    # DRF API endpoints (un-namespaced names like 'business-list', 'business-detail')
    path("api/v1/", include(businesses_router.urls)),
    # Non-router business endpoints used by the static frontend
    path("api/v1/search/", business_views.business_search_html, name="business_search_html"),
    path(
        "api/v1/businesses/<int:business_id>/card/",
        business_views.business_card_html,
        name="business_card_html",
    ),
    path(
        "api/v1/businesses/<int:business_id>/detail_html/",
        business_views.business_detail_html,
        name="business_detail_html",
    ),
    path(
        "api/v1/businesses/<int:business_id>/fragment/",
        business_views.business_detail_html,
        name="business_fragment_html",
    ),
    path(
        "api/v1/business-locations/",
        business_views.business_locations,
        name="business_locations",
    ),
    path(
        "businesses/",
        include(("apps.businesses.urls", "businesses"), namespace="businesses"),
    ),
    path(
        "api/v1/accounts/",
        include(("apps.accounts.urls", "accounts"), namespace="accounts"),
    ),
    # We'll add more API endpoints here later
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
