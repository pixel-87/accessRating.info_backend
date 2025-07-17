from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from .models import Business, BusinessPhoto, BusinessReview
from .serializers import BusinessSerializer, BusinessPhotoSerializer, BusinessReviewSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    """ViewSet for managing businesses"""
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_type', 'accessibility_level', 'city', 'is_verified']
    search_fields = ['name', 'description', 'address', 'city']
    ordering_fields = ['name', 'created_at', 'accessibility_level']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by owner='me' to get current user's businesses
        owner = self.request.query_params.get('owner')
        if owner == 'me' and self.request.user.is_authenticated:
            queryset = queryset.filter(owner=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating a business"""
        serializer.save(owner=self.request.user)
    
    def perform_update(self, serializer):
        """Only allow owners to update their businesses"""
        business = self.get_object()
        if business.owner != self.request.user:
            # Admins can update any business, regular users only their own
            if not self.request.user.is_staff:
                raise PermissionError("You can only edit your own businesses")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only allow owners to delete their businesses"""
        if instance.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionError("You can only delete your own businesses")
        super().perform_destroy(instance)

    @action(detail=True, methods=['get'], permission_classes=[])
    def qr_code(self, request, pk=None):
        """Generate QR code for the business"""
        business = self.get_object()
        base_url = request.build_absolute_uri('/').rstrip('/')
        
        try:
            # Generate QR code image
            qr_image_buffer = business.generate_qr_code_image(base_url)
            
            # Return as image response
            response = HttpResponse(qr_image_buffer.getvalue(), content_type='image/png')
            response['Content-Disposition'] = f'inline; filename="qr_code_{business.id}.png"'
            return response
        except Exception as e:
            return Response({'error': f'Failed to generate QR code: {str(e)}'}, status=500)
    
    @action(detail=True, methods=['get'], permission_classes=[])
    def qr_url(self, request, pk=None):
        """Get the URL that the QR code links to"""
        business = self.get_object()
        base_url = request.build_absolute_uri('/').rstrip('/')
        
        return Response({
            'qr_url': business.generate_qr_code_url(),
            'business_url': f"{base_url}/business/{business.id}",
            'qr_data': business.generate_qr_code_data()
        })


class BusinessPhotoViewSet(viewsets.ModelViewSet):
    """ViewSet for managing business photos"""
    queryset = BusinessPhoto.objects.all()
    serializer_class = BusinessPhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Set the uploaded_by to the current user when creating a photo"""
        serializer.save(uploaded_by=self.request.user)


class BusinessReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing business reviews"""
    queryset = BusinessReview.objects.all()
    serializer_class = BusinessReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['business', 'rating', 'is_approved']
    
    def perform_create(self, serializer):
        """Set the reviewer to the current user when creating a review"""
        serializer.save(reviewer=self.request.user)
