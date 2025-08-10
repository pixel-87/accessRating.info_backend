"""
Tests for the businesses app URLs.
"""

from apps.businesses.models import Business
from apps.businesses.views import BusinessViewSet
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse


class BusinessURLsTest(TestCase):
    """Test cases for businesses app URL patterns."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.business = Business.objects.create(
            owner=self.user,
            name="Test Business",
            address="123 Test Street",
            postcode="SW1A 1AA",
            city="London",
            business_type="cafe",
        )

    def test_business_list_url_resolves(self):
        """Test that business list URL resolves to correct view."""
        url = reverse("business-list")
        self.assertEqual(url, "/api/v1/businesses/")

        resolver = resolve("/api/v1/businesses/")
        self.assertEqual(resolver.func.cls, BusinessViewSet)

    def test_business_detail_url_resolves(self):
        """Test that business detail URL resolves to correct view."""
        url = reverse("business-detail", kwargs={"pk": self.business.pk})
        self.assertEqual(url, f"/api/v1/businesses/{self.business.pk}/")

        resolver = resolve(f"/api/v1/businesses/{self.business.pk}/")
        self.assertEqual(resolver.func.cls, BusinessViewSet)

    def test_business_list_url_name(self):
        """Test business list URL name is correct."""
        url = reverse("business-list")
        self.assertEqual(url, "/api/v1/businesses/")

    def test_business_detail_url_name(self):
        """Test business detail URL name is correct."""
        url = reverse("business-detail", args=[self.business.pk])
        self.assertEqual(url, f"/api/v1/businesses/{self.business.pk}/")

    def test_business_urls_namespace(self):
        """Test that business URLs are properly configured."""
        # Test various URL patterns that should work
        list_url = reverse("business-list")
        detail_url = reverse("business-detail", kwargs={"pk": 1})

        self.assertTrue(list_url.startswith("/api/v1/businesses/"))
        self.assertTrue(detail_url.startswith("/api/v1/businesses/"))

    def test_url_patterns_coverage(self):
        """Test that all expected URL patterns are available."""
        # These should all resolve without error
        business_id = self.business.pk

        urls_to_test = [
            ("business-list", {}),
            ("business-detail", {"pk": business_id}),
        ]

        for url_name, kwargs in urls_to_test:
            with self.subTest(url_name=url_name):
                url = reverse(url_name, kwargs=kwargs)
                self.assertIsNotNone(url)
                # Should not raise an exception
                resolved = resolve(url)
                self.assertIsNotNone(resolved)
