from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.businesses.models import Business


class BusinessFragmentViewTest(APITestCase):
    """Tests for the business fragment endpoint used by HTMX."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="fraguser", password="testpass123" #pragma: allowlist secret
        )
        self.business = Business.objects.create(
            owner=self.user,
            name="Fragment Test Business",
            address="1 Fragment Lane",
            postcode="SW1A 1AA",
            city="Testville",
            business_type="cafe",
            accessibility_level=4,
        )

    def test_fragment_returns_html(self):
        url = reverse(
            "businesses:business_fragment_html",
            kwargs={"business_id": self.business.id},
        )
        # The fragment view is a plain Django view that returns HTML
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.content.decode("utf-8")
        # it should include the business name
        self.assertIn(self.business.name, content)
