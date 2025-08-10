from datetime import date

from apps.accounts.models import UserFavorite, UserProfile, UserSearchHistory
from apps.businesses.models import Business
from django.contrib.auth.models import User
from django.test import TestCase


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_user_profile_creation(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            user_type="business",
            phone="+441234567890",
            bio="Test bio",
            business_license_number="BL123456",
        )

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.user_type, "business")
        self.assertEqual(profile.phone, "+441234567890")
        self.assertTrue(profile.is_business_owner)
        self.assertFalse(profile.is_assessor)
        self.assertFalse(profile.can_assess_businesses)

    def test_assessor_profile(self):
        """Test assessor profile functionality"""
        profile = UserProfile.objects.create(
            user=self.user,
            user_type="assessor",
            assessor_training_completed=True,
            assessor_certification_date=date.today(),
        )

        self.assertTrue(profile.is_assessor)
        self.assertTrue(profile.can_assess_businesses)

    def test_assessor_without_training(self):
        """Test assessor without completed training"""
        profile = UserProfile.objects.create(
            user=self.user, user_type="assessor", assessor_training_completed=False
        )

        self.assertTrue(profile.is_assessor)
        self.assertFalse(profile.can_assess_businesses)

    def test_profile_str_method(self):
        """Test string representation of profile"""
        profile = UserProfile.objects.create(user=self.user, user_type="regular")

        expected = f"{self.user.username} - Regular User"
        self.assertEqual(str(profile), expected)


class UserFavoriteModelTest(TestCase):
    """Test cases for UserFavorite model"""

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
        )

    def test_favorite_creation(self):
        """Test creating a favorite"""
        favorite = UserFavorite.objects.create(user=self.user, business=self.business)

        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.business, self.business)
        self.assertTrue(favorite.created_at)

    def test_favorite_str_method(self):
        """Test string representation of favorite"""
        favorite = UserFavorite.objects.create(user=self.user, business=self.business)

        expected = f"{self.user.username} favorited {self.business.name}"
        self.assertEqual(str(favorite), expected)

    def test_unique_constraint(self):
        """Test unique constraint on user-business combination"""
        UserFavorite.objects.create(user=self.user, business=self.business)

        # Attempting to create duplicate should raise IntegrityError
        with self.assertRaises(Exception):
            UserFavorite.objects.create(user=self.user, business=self.business)


class UserSearchHistoryModelTest(TestCase):
    """Test cases for UserSearchHistory model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_search_history_creation(self):
        """Test creating search history"""
        search = UserSearchHistory.objects.create(
            user=self.user,
            search_query="accessible cafes",
            search_location="London",
            business_type_filter="cafe",
            accessibility_filter=3,
        )

        self.assertEqual(search.user, self.user)
        self.assertEqual(search.search_query, "accessible cafes")
        self.assertEqual(search.search_location, "London")
        self.assertEqual(search.business_type_filter, "cafe")
        self.assertEqual(search.accessibility_filter, 3)

    def test_search_history_str_method(self):
        """Test string representation of search history"""
        search = UserSearchHistory.objects.create(
            user=self.user, search_query="accessible restaurants"
        )

        expected = f"{self.user.username} searched for 'accessible restaurants'"
        self.assertEqual(str(search), expected)
