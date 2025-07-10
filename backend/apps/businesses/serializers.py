"""
Serializers for the businesses app.
"""
from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    """
    Serializer for the Business model.
    """
    
    # Read-only fields that are computed or set automatically
    owner = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    accessibility_level_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'id',
            'name', 
            'description',
            'address',
            'postcode',
            'city',
            'latitude',        # Essential for Google Maps
            'longitude',       # Essential for Google Maps
            'business_type',
            'specialisation',
            'phone',
            'email',
            'website',
            'opening_times',
            'accessibility_level',
            'accessibility_level_display',
            'accessibility_features',
            'accessibility_barriers',
            'first_assessed_date',
            'next_assessment_date',
            'owner',
            'created_at',
            'updated_at',
            'is_verified',
            'sticker_requested',
            'sticker_type',
            'business_notes',
            'special_mentions',
        ]
        read_only_fields = [
            'id', 'owner', 'created_at', 'updated_at', 'is_verified', 
            'first_assessed_date', 'next_assessment_date'
        ]
    
    def create(self, validated_data):
        """
        Create a new Business instance.
        """
        business = Business(**validated_data)
        business.save()
        return business
    
    def update(self, instance, validated_data):
        """
        Update a Business instance.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class BusinessCreateSerializer(BusinessSerializer):
    """
    Serializer for creating businesses with required fields only.
    """
    
    class Meta(BusinessSerializer.Meta):
        fields = [
            'name', 
            'description',
            'address',
            'postcode',
            'city',
            'latitude',
            'longitude',
            'what3words',
            'business_type',
            'specialisation',
            'phone',
            'email',
            'website',
            'opening_times',
            'accessibility_level',
            'accessibility_features',
            'accessibility_barriers',
            'business_notes',
            'special_mentions',
        ]


class BusinessListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing businesses (less data).
    """
    
    owner = serializers.StringRelatedField(read_only=True)
    accessibility_level_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'id',
            'name',
            'city',
            'postcode',
            'business_type',
            'accessibility_level',
            'accessibility_level_display',
            'owner',
            'created_at',
            'is_verified',
        ]
