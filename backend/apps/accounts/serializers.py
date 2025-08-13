from django.contrib.auth.models import User
from rest_framework import serializers
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as BaseRegisterSerializer,
)

from .models import UserFavorite, UserProfile, UserSearchHistory


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile data"""

    class Meta:
        model = UserProfile
        fields = [
            "user_type",
            "phone",
            "bio",
            "accessibility_needs",
            "business_license_number",
            "assessor_training_completed",
            "assessor_certification_date",
            "email_notifications",
            "profile_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data with profile"""

    profile = UserProfileSerializer(read_only=True)
    business_count = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
            "is_active",
            "profile",
            "business_count",
            "favorite_count",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]

    def get_business_count(self, obj):
        """Get count of businesses owned by this user"""
        return obj.businesses.count()

    def get_favorite_count(self, obj):
        """Get count of businesses favorited by this user"""
        return obj.favorites.count()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "profile"]

    def update(self, instance, validated_data):
        # Handle profile data separately
        profile_data = validated_data.pop("profile", {})

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create profile
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class UserFavoriteSerializer(serializers.ModelSerializer):
    """Serializer for user favorites"""

    business_name = serializers.CharField(source="business.name", read_only=True)
    business_accessibility_level = serializers.IntegerField(
        source="business.accessibility_level",
        read_only=True,
    )
    business_city = serializers.CharField(source="business.city", read_only=True)
    business_type = serializers.CharField(
        source="business.business_type",
        read_only=True,
    )

    class Meta:
        model = UserFavorite
        fields = [
            "id",
            "business",
            "business_name",
            "business_accessibility_level",
            "business_city",
            "business_type",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class UserSearchHistorySerializer(serializers.ModelSerializer):
    """Serializer for user search history"""

    class Meta:
        model = UserSearchHistory
        fields = [
            "id",
            "search_query",
            "search_location",
            "business_type_filter",
            "accessibility_filter",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class RegisterSerializer(BaseRegisterSerializer):
    """Custom registration serializer with phone field support for allauth adapter."""

    _has_phone_field = False  # Ensure this is always present as a class attribute

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_phone_field = False  # Set to True if you add a phone field
