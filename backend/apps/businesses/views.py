"""
Views for the businesses app.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Business
from .serializers import BusinessSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Business instances.
    Provides CRUD operations for businesses.
    """
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    
    # Add filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['accessibility_level', 'business_type', 'city']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['name', 'created_at', 'updated_at', 'accessibility_level']
    ordering = ['-created_at']  # Default ordering
    
    def perform_create(self, serializer):
        """
        Override to set the owner of the business to the current user.
        """
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """
        Optionally restrict the returned businesses to those owned by the user,
        by filtering against a `owner` query parameter in the URL.
        """
        queryset = Business.objects.all()
        owner = self.request.query_params.get('owner')
        if owner is not None:
            if owner.lower() == 'me':
                queryset = queryset.filter(owner=self.request.user)
            else:
                queryset = queryset.filter(owner__username=owner)
        return queryset
