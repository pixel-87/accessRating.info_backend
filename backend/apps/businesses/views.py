from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Business
from .serializers import BusinessListSerializer, BusinessDetailSerializer, BusinessCreateSerializer


class BusinessListView(generics.ListCreateAPIView):
    """
    List all businesses or create a new business
    """
    queryset = Business.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_type', 'accessibility_rating', 'postcode']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['name', 'created_at', 'accessibility_rating']
    ordering = ['-created_at']  # Default ordering
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BusinessCreateSerializer
        return BusinessListSerializer
    
    def perform_create(self, serializer):
        # For MVP, anyone can create a business
        # Later we can add business owner claiming
        serializer.save()


class BusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a business
    """
    queryset = Business.objects.all()
    serializer_class = BusinessDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """
        Only allow business owners or admins to modify
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # For MVP, only authenticated users can edit
            # Later add business ownership checks
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def business_qr_view(request, business_id):
    """
    Generate QR code data for a business
    """
    business = get_object_or_404(Business, id=business_id, is_active=True)
    
    # QR code data
    qr_data = {
        'business_id': str(business.id),
        'name': business.name,
        'accessibility_rating': business.accessibility_rating,
        'rating_display': business.get_accessibility_rating_display() if business.accessibility_rating else None,
        'address': business.address,
        'url': request.build_absolute_uri(f'/business/{business.id}/')
    }
    
    return Response(qr_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def business_stats_view(request):
    """
    Get business statistics for dashboard
    """
    from django.db.models import Count, Avg
    
    stats = {
        'total_businesses': Business.objects.filter(is_active=True).count(),
        'rated_businesses': Business.objects.filter(
            is_active=True, 
            accessibility_rating__isnull=False
        ).count(),
        'average_rating': Business.objects.filter(
            accessibility_rating__isnull=False
        ).aggregate(avg_rating=Avg('accessibility_rating'))['avg_rating'],
        'businesses_by_type': Business.objects.filter(
            is_active=True
        ).values('business_type').annotate(count=Count('id')),
        'businesses_by_rating': Business.objects.filter(
            is_active=True,
            accessibility_rating__isnull=False
        ).values('accessibility_rating').annotate(count=Count('id'))
    }
    
    return Response(stats)
