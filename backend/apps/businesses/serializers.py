from rest_framework import serializers
from .models import Business


class BusinessListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for business list view
    """
    accessibility_rating_display = serializers.CharField(source='get_accessibility_rating_display', read_only=True)
    business_type_display = serializers.CharField(source='get_business_type_display', read_only=True)
    has_accessibility_rating = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'id',
            'name',
            'business_type',
            'business_type_display',
            'accessibility_rating',
            'accessibility_rating_display',
            'has_accessibility_rating',
            'address',
            'postcode',
            'is_active',
            'created_at'
        ]


class BusinessDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for business detail view
    """
    accessibility_rating_display = serializers.CharField(source='get_accessibility_rating_display', read_only=True)
    business_type_display = serializers.CharField(source='get_business_type_display', read_only=True)
    has_accessibility_rating = serializers.BooleanField(read_only=True)
    qr_code_url = serializers.CharField(read_only=True)
    public_url = serializers.CharField(read_only=True)
    
    # Read-only fields for security
    claimed_by_username = serializers.CharField(source='claimed_by.username', read_only=True)
    assessed_by_username = serializers.CharField(source='assessed_by.username', read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'id',
            'name',
            'description',
            'business_type',
            'business_type_display',
            'email',
            'phone',
            'website',
            'address',
            'postcode',
            'latitude',
            'longitude',
            'what3words',
            'accessibility_rating',
            'accessibility_rating_display',
            'has_accessibility_rating',
            'last_assessed',
            'assessment_notes',
            'claimed_by_username',
            'assessed_by_username',
            'is_verified',
            'is_active',
            'qr_code_url',
            'public_url',
            'created_at',
            'updated_at'
        ]


class BusinessCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new businesses
    """
    class Meta:
        model = Business
        fields = [
            'name',
            'description',
            'business_type',
            'email',
            'phone',
            'website',
            'address',
            'postcode',
            'latitude',
            'longitude',
            'what3words',
        ]
    
    def validate_name(self, value):
        """
        Check that business name is not already taken in the same postcode
        """
        postcode = self.initial_data.get('postcode')
        if postcode and Business.objects.filter(name=value, postcode=postcode).exists():
            raise serializers.ValidationError(
                "A business with this name already exists in this postcode."
            )
        return value
