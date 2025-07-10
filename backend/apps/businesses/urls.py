from django.urls import path
from . import views

urlpatterns = [
    # Business CRUD endpoints
    path('', views.BusinessListView.as_view(), name='business-list'),
    path('<uuid:pk>/', views.BusinessDetailView.as_view(), name='business-detail'),
    
    # QR Code endpoint
    path('<uuid:business_id>/qr/', views.business_qr_view, name='business-qr'),
    
    # Statistics endpoint
    path('stats/', views.business_stats_view, name='business-stats'),
]
