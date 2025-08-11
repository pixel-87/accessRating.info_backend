"""
Tests for the businesses app views.
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.businesses.models import Business


class BusinessViewSetTest(APITestCase):
    """Test cases for BusinessViewSet API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

        # Create JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.business_data = {
            "name": "Test Business",
            "description": "A test business for accessibility",
            "address": "123 Test Street",
            "postcode": "SW1A 1AA",
            "city": "London",
            "business_type": "cafe",
            "accessibility_level": 3,
        }

        self.business = Business.objects.create(
            owner=self.user, **self.business_data
        )

    def authenticate(self):
        """Authenticate the test client using JWT"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def test_list_businesses_authenticated(self):
        """Test retrieving list of businesses when authenticated."""
        self.authenticate()
        url = reverse("business-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Test Business")

    def test_list_businesses_unauthenticated(self):
        """Test retrieving list of businesses when not authenticated."""
        url = reverse("business-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Test Business")

    def test_create_business_authenticated(self):
        """Test creating a business when authenticated."""
        self.authenticate()
        url = reverse("business-list")

        new_business_data = {
            "name": "New Test Business",
            "description": "Another test business",
            "address": "456 New Street",
            "postcode": "W1A 1AA",
            "city": "London",
            "business_type": "restaurant",
            "accessibility_level": 2,
        }

        response = self.client.post(url, new_business_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Test Business")
        self.assertEqual(response.data["owner"], "testuser")

    def test_create_business_unauthenticated(self):
        """Test creating a business when not authenticated."""
        url = reverse("business-list")
        response = self.client.post(url, self.business_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_business(self):
        """Test retrieving a specific business."""
        self.authenticate()
        url = reverse("business-detail", kwargs={"pk": self.business.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Business")

    def test_update_business_as_owner(self):
        """Test updating a business as the owner."""
        self.authenticate()
        url = reverse("business-detail", kwargs={"pk": self.business.pk})

        update_data = {
            "name": "Updated Business Name",
            "description": "Updated description",
            "address": self.business.address,
            "postcode": self.business.postcode,
            "city": self.business.city,
            "business_type": self.business.business_type,
            "accessibility_level": 4,
        }

        response = self.client.patch(url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Business Name")
        self.assertEqual(response.data["accessibility_level"], 4)

    def test_delete_business_as_owner(self):
        """Test deleting a business as the owner."""
        self.authenticate()
        url = reverse("business-detail", kwargs={"pk": self.business.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Business.objects.filter(pk=self.business.pk).exists())

    def test_filter_by_accessibility_level(self):
        """Test filtering businesses by accessibility level."""
        # Create another business with different accessibility level
        Business.objects.create(
            owner=self.user,
            name="Another Business",
            accessibility_level=5,
            address="789 Filter Street",
            postcode="E1A 1AA",
            city="London",
            business_type="shop",
        )

        self.authenticate()
        url = reverse("business-list")
        response = self.client.get(url, {"accessibility_level": 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["accessibility_level"], 3)

    def test_search_businesses(self):
        """Test searching businesses by name."""
        self.authenticate()
        url = reverse("business-list")
        response = self.client.get(url, {"search": "Test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Test Business")

    def test_filter_businesses_by_owner_me(self):
        """Test filtering businesses by owner='me'."""
        # Create another user and business
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        Business.objects.create(
            owner=other_user,
            name="Other User Business",
            address="999 Other Street",
            postcode="N1A 1AA",
            city="London",
            business_type="pub",
        )

        self.authenticate()
        url = reverse("business-list")
        response = self.client.get(url, {"owner": "me"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["owner"], "testuser")
