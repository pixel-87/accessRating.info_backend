from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from apps.accounts.models import UserFavorite, UserProfile, UserSearchHistory
from apps.accounts.serializers import (UserFavoriteSerializer,
                                       UserProfileSerializer,
                                       UserSearchHistorySerializer,
                                       UserSerializer, UserUpdateSerializer)
from apps.businesses.models import Business


class UserProfileSerializerTest(TestCase):
    """Test cases for UserProfileSerializer"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            user_type="business",
            phone="+441234567890",
            bio="Test bio",
            business_license_number="BL123456",
            assessor_training_completed=True,
            assessor_certification_date=date.today(),
        )

    def test_profile_serialization(self):
        """Test serializing user profile"""
        serializer = UserProfileSerializer(instance=self.profile)
        data = serializer.data

        self.assertEqual(data["user_type"], "business")
        self.assertEqual(data["phone"], "+441234567890")
        self.assertEqual(data["bio"], "Test bio")
        self.assertEqual(data["business_license_number"], "BL123456")
        self.assertTrue(data["assessor_training_completed"])
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_profile_deserialization(self):
        """Test deserializing user profile data"""
        data = {
            "user_type": "assessor",
            "phone": "+447890123456",
            "bio": "New bio",
            "accessibility_needs": "Wheelchair access required",
            "assessor_training_completed": True,
        }

        serializer = UserProfileSerializer(instance=self.profile, data=data)
        self.assertTrue(serializer.is_valid())

        updated_profile = serializer.save()
        self.assertEqual(updated_profile.user_type, "assessor")
        self.assertEqual(updated_profile.phone, "+447890123456")
        self.assertEqual(
            updated_profile.accessibility_needs, "Wheelchair access required"
        )


class UserSerializerTest(TestCase):
    """Test cases for UserSerializer"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        self.profile = UserProfile.objects.create(user=self.user, user_type="regular")

        # Create a business owned by user
        self.business = Business.objects.create(
            name="Test Business",
            address="123 Test St",
            postcode="SW1A 1AA",
            city="London",
            business_type="cafe",
            owner=self.user,
        )

        # Create a favorite
        UserFavorite.objects.create(user=self.user, business=self.business)

    def test_user_serialization(self):
        """Test serializing user with profile"""
        serializer = UserSerializer(instance=self.user)
        data = serializer.data

        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["first_name"], "Test")
        self.assertEqual(data["last_name"], "User")
        self.assertEqual(data["profile"]["user_type"], "regular")
        self.assertEqual(data["business_count"], 1)
        self.assertEqual(data["favorite_count"], 1)


class UserUpdateSerializerTest(TestCase):
    """Test cases for UserUpdateSerializer"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        self.profile = UserProfile.objects.create(user=self.user, user_type="regular")

    def test_user_update_with_profile(self):
        """Test updating user and profile data"""
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com",
            "profile": {
                "user_type": "business",
                "phone": "+441234567890",
                "bio": "Updated bio",
            },
        }

        serializer = UserUpdateSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid())

        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "Name")
        self.assertEqual(updated_user.email, "updated@example.com")

        # Check profile was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user_type, "business")
        self.assertEqual(self.profile.phone, "+441234567890")
        self.assertEqual(self.profile.bio, "Updated bio")

    def test_user_update_creates_profile(self):
        """Test updating user creates profile if it doesn't exist"""
        # Create user without profile
        new_user = User.objects.create_user(
            username="newuser", email="new@example.com", password="password123"
        )

        data = {
            "first_name": "New",
            "profile": {"user_type": "assessor", "bio": "New assessor"},
        }

        serializer = UserUpdateSerializer(instance=new_user, data=data)
        self.assertTrue(serializer.is_valid())

        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, "New")

        # Check profile was created
        profile = UserProfile.objects.get(user=new_user)
        self.assertEqual(profile.user_type, "assessor")
        self.assertEqual(profile.bio, "New assessor")


class UserFavoriteSerializerTest(TestCase):
    """Test cases for UserFavoriteSerializer"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.business = Business.objects.create(
            name="Test Cafe",
            address="123 Test Street",
            postcode="SW1A 1AA",
            city="London",
            business_type="cafe",
            accessibility_level=4,
        )

        self.favorite = UserFavorite.objects.create(
            user=self.user, business=self.business
        )

    def test_favorite_serialization(self):
        """Test serializing user favorite"""
        serializer = UserFavoriteSerializer(instance=self.favorite)
        data = serializer.data

        self.assertEqual(data["business"], self.business.id)
        self.assertEqual(data["business_name"], "Test Cafe")
        self.assertEqual(data["business_accessibility_level"], 4)
        self.assertEqual(data["business_city"], "London")
        self.assertEqual(data["business_type"], "cafe")
        self.assertIn("created_at", data)


class UserSearchHistorySerializerTest(TestCase):
    """Test cases for UserSearchHistorySerializer"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.search = UserSearchHistory.objects.create(
            user=self.user,
            search_query="accessible cafes",
            search_location="London",
            business_type_filter="cafe",
            accessibility_filter=3,
        )

    def test_search_history_serialization(self):
        """Test serializing search history"""
        serializer = UserSearchHistorySerializer(instance=self.search)
        data = serializer.data

        self.assertEqual(data["search_query"], "accessible cafes")
        self.assertEqual(data["search_location"], "London")
        self.assertEqual(data["business_type_filter"], "cafe")
        self.assertEqual(data["accessibility_filter"], 3)
        self.assertIn("created_at", data)

    def test_search_history_deserialization(self):
        """Test deserializing search history data"""
        data = {
            "search_query": "accessible restaurants",
            "search_location": "Manchester",
            "business_type_filter": "restaurant",
            "accessibility_filter": 5,
        }

        serializer = UserSearchHistorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

        # Note: We don't save here as user field would be missing
        # In actual usage, user is set in the view's perform_create method
