from rest_framework import serializers
from .models import Business, BusinessPhoto, BusinessReview


class BusinessPhotoSerializer(serializers.ModelSerializer):
    """Serializer for business photos"""
    uploaded_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = BusinessPhoto
        fields = [
            'id', 'photo', 'photo_type', 'caption', 
            'created_at', 'is_primary', 'uploaded_by'
        ]
        read_only_fields = ['id', 'created_at', 'uploaded_by']


class BusinessReviewSerializer(serializers.ModelSerializer):
    """Serializer for business reviews"""
    reviewer = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = BusinessReview
        fields = [
            'id', 'rating', 'comment', 'photo', 'created_at', 
            'updated_at', 'is_approved', 'reviewer'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'reviewer']


class BusinessSerializer(serializers.ModelSerializer):
    """Serializer for businesses"""
    owner = serializers.StringRelatedField(read_only=True)
    photos = BusinessPhotoSerializer(many=True, read_only=True)
    reviews = BusinessReviewSerializer(many=True, read_only=True)
    accessibility_level_display = serializers.CharField(read_only=True)
    is_accessible = serializers.BooleanField(read_only=True)
    has_location_data = serializers.BooleanField(read_only=True)
    needs_reassessment = serializers.BooleanField(read_only=True)
    full_business_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'description', 'address', 'postcode', 'city',
            'latitude', 'longitude', 'what3words', 'business_type', 
            'specialisation', 'phone', 'email', 'website', 'opening_times',
            'accessibility_level', 'accessibility_features', 'accessibility_barriers',
            'access_report', 'first_assessed_date', 'next_assessment_date',
            'created_at', 'updated_at', 'is_verified', 'sticker_requested',
            'sticker_type', 'business_notes', 'special_mentions', 'owner',
            'photos', 'reviews', 'accessibility_level_display', 'is_accessible',
            'has_location_data', 'needs_reassessment', 'full_business_type'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'owner', 'photos', 'reviews',
            'accessibility_level_display', 'is_accessible', 'has_location_data',
            'needs_reassessment', 'full_business_type'
        ]
    
    def get_full_business_type(self, obj):
        """Get business type with specialisation"""
        return obj.get_full_business_type()
    
    def create(self, validated_data):
        """Create business with current user as owner"""
        # Only set owner if we have a request context
        if self.context.get('request') and hasattr(self.context['request'], 'user'):
            validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)