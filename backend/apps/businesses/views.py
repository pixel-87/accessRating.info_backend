from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
import math
from .models import Business, BusinessPhoto, BusinessReview
from .serializers import BusinessSerializer, BusinessPhotoSerializer, BusinessReviewSerializer


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in miles
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in miles
    r = 3956
    return c * r


# API endpoint for business locations (for map) with filtering support
def business_locations(request):
    """
    Return filtered business locations for map display
    
    Supported filters:
    - min_rating: minimum accessibility rating (1-5)
    - max_rating: maximum accessibility rating (1-5)
    - business_type: type of business (cafe, restaurant, pub, etc.)
    - lat, lng, radius: center point and radius in miles for distance filtering
    - search: text search in name, description, address
    """
    businesses = Business.objects.filter(latitude__isnull=False, longitude__isnull=False)
    
    # Filter by minimum accessibility rating
    min_rating = request.GET.get('min_rating')
    if min_rating:
        try:
            min_rating = int(min_rating)
            if 1 <= min_rating <= 5:
                businesses = businesses.filter(accessibility_level__gte=min_rating)
        except (ValueError, TypeError):
            pass
    
    # Filter by maximum accessibility rating
    max_rating = request.GET.get('max_rating')
    if max_rating:
        try:
            max_rating = int(max_rating)
            if 1 <= max_rating <= 5:
                businesses = businesses.filter(accessibility_level__lte=max_rating)
        except (ValueError, TypeError):
            pass
    
    # Filter by business type
    business_type = request.GET.get('business_type')
    if business_type and business_type != 'all':
        businesses = businesses.filter(business_type=business_type)
    
    # Text search filter
    search = request.GET.get('search', '').strip()
    if search:
        businesses = businesses.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(address__icontains=search) |
            Q(city__icontains=search)
        )
    
    # Distance filtering
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius')
    
    filtered_businesses = []
    
    if lat and lng and radius:
        try:
            center_lat = float(lat)
            center_lng = float(lng)
            max_distance = float(radius)
            
            # Filter by distance
            for business in businesses:
                if business.latitude and business.longitude:
                    distance = haversine_distance(
                        center_lat, center_lng,
                        float(business.latitude), float(business.longitude)
                    )
                    if distance <= max_distance:
                        filtered_businesses.append({
                            "id": business.id,
                            "name": business.name,
                            "latitude": float(business.latitude),
                            "longitude": float(business.longitude),
                            "address": business.address,
                            "business_type": business.business_type,
                            "accessibility_level": business.accessibility_level,
                            "distance": round(distance, 2)
                        })
        except (ValueError, TypeError):
            # If distance filtering fails, fall back to normal filtering
            filtered_businesses = [
                {
                    "id": b.id,
                    "name": b.name,
                    "latitude": float(b.latitude),
                    "longitude": float(b.longitude),
                    "address": b.address,
                    "business_type": b.business_type,
                    "accessibility_level": b.accessibility_level,
                }
                for b in businesses
            ]
    else:
        # No distance filtering - return all matching businesses
        filtered_businesses = [
            {
                "id": b.id,
                "name": b.name,
                "latitude": float(b.latitude),
                "longitude": float(b.longitude),
                "address": b.address,
                "business_type": b.business_type,
                "accessibility_level": b.accessibility_level,
            }
            for b in businesses
        ]
    
    return JsonResponse(filtered_businesses, safe=False)


# API endpoint for a single business card (for map popup/panel)
def business_card_html(request, business_id):
    """Return HTML fragment for a single business card (for map popup/panel)"""
    business = get_object_or_404(Business, id=business_id)
    return render(request, 'businesses/business_card.html', {'business': business})


@csrf_exempt
def business_search_html(request):
    """Return HTML fragments for HTMX business search"""
    search_query = request.GET.get('search', '').strip()
    
    # Start with all businesses
    businesses = Business.objects.all()
    
    # Apply search if provided
    if search_query:
        businesses = businesses.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(accessibility_features__icontains=search_query) |
            Q(specialisation__icontains=search_query)
        )
    
    # Order by accessibility level (highest first) then name
    businesses = businesses.order_by('-accessibility_level', 'name')
    
    # Render the template with businesses
    return render(request, 'businesses/business_cards.html', {
        'businesses': businesses,
        'search_query': search_query
    })


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
