from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
