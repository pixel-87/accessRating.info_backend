"""
Tests for Business models.
"""

from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.businesses.models import Business, BusinessPhoto, BusinessReview


class BusinessModelTest(TestCase):
    """Test cases for the Business model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testowner", email="owner@example.com", password="testpass123"
        )

        self.business_data = {
            "name": "Test Cafe",
            "description": "A friendly local cafe with good accessibility features.",
            "address": "123 Test Street, Test Town",
            "postcode": "SW1A 1AA",
            "city": "London",
            "latitude": 51.507351,
            "longitude": -0.127758,
            "business_type": "cafe",
            "specialisation": "Italian",
            "phone": "020 1234 5678",
            "email": "info@testcafe.co.uk",
            "accessibility_level": 3,
            "owner": self.user,
        }

    def test_business_creation(self):
        """Test creating a business with valid data."""
        business = Business.objects.create(**self.business_data)

        self.assertEqual(business.name, "Test Cafe")
        self.assertEqual(business.business_type, "cafe")
        self.assertEqual(business.specialisation, "Italian")
        self.assertEqual(business.accessibility_level, 3)
        self.assertEqual(business.owner, self.user)
        self.assertIsNotNone(business.id)
        self.assertIsInstance(business.id, int)  # AutoField should be integer

    def test_business_str_representation(self):
        """Test string representation of business."""
        business = Business.objects.create(**self.business_data)
        expected = f"{business.name} - {business.city}"
        self.assertEqual(str(business), expected)

    def test_postcode_validation(self):
        """Test UK postcode validation."""
        # Valid postcode should work
        business = Business.objects.create(**self.business_data)
        self.assertEqual(business.postcode, "SW1A 1AA")

        # Invalid postcode should raise ValidationError
        invalid_data = self.business_data.copy()
        invalid_data["postcode"] = "INVALID"

        business = Business(**invalid_data)
        with self.assertRaises(ValidationError):
            business.full_clean()

    def test_accessibility_level_choices(self):
        """Test accessibility level choices."""
        # Create test data without coordinates to avoid decimal validation issues
        test_data = self.business_data.copy()
        test_data.pop("latitude", None)
        test_data.pop("longitude", None)
        business = Business.objects.create(**test_data)

        # Test valid choices
        for level in [1, 2, 3, 4, 5]:
            business.accessibility_level = level
            business.full_clean()  # Should not raise ValidationError

        # Test invalid choice
        business.accessibility_level = 6
        with self.assertRaises(ValidationError):
            business.full_clean()

    def test_get_full_business_type(self):
        """Test business type with specialisation."""
        business = Business.objects.create(**self.business_data)
        self.assertEqual(business.get_full_business_type(), "Italian Cafe")

        # Test without specialisation
        business.specialisation = ""
        self.assertEqual(business.get_full_business_type(), "Cafe")

    def test_accessibility_level_display(self):
        """Test accessibility level display property."""
        business = Business.objects.create(**self.business_data)
        self.assertIn("Rating 3", business.accessibility_level_display)

        # Test unrated business
        business.accessibility_level = None
        self.assertEqual(business.accessibility_level_display, "Not rated")

    def test_is_accessible_property(self):
        """Test is_accessible property."""
        business = Business.objects.create(**self.business_data)

        # Rating 3 should be accessible
        business.accessibility_level = 3
        self.assertTrue(business.is_accessible)

        # Rating 2 should not be accessible
        business.accessibility_level = 2
        self.assertFalse(business.is_accessible)

        # No rating should not be accessible
        business.accessibility_level = None
        self.assertFalse(business.is_accessible)

    def test_needs_reassessment_property(self):
        """Test needs_reassessment property."""
        business = Business.objects.create(**self.business_data)

        # No assessment dates
        self.assertFalse(business.needs_reassessment)

        # Assessment in future
        business.first_assessed_date = timezone.now() - timedelta(days=30)
        business.next_assessment_date = timezone.now() + timedelta(days=30)
        self.assertFalse(business.needs_reassessment)

        # Assessment overdue
        business.next_assessment_date = timezone.now() - timedelta(days=30)
        self.assertTrue(business.needs_reassessment)

    def test_generate_qr_code_data(self):
        """Test QR code data generation."""
        business = Business.objects.create(**self.business_data)
        qr_data = business.generate_qr_code_data()

        self.assertIn(str(business.id), qr_data)
        self.assertIn("Test_Cafe", qr_data)
        self.assertTrue(qr_data.startswith("business_id_"))

    def test_has_location_data_property(self):
        """Test has_location_data property."""
        business = Business.objects.create(**self.business_data)

        # Should have location data due to default coordinates
        self.assertTrue(business.has_location_data)

        # Verify default coordinates are London center
        self.assertEqual(float(business.latitude), 51.507351)
        self.assertEqual(float(business.longitude), -0.127758)

        # Test with custom coordinates
        business.latitude = 51.5074
        business.longitude = -0.1278
        self.assertTrue(business.has_location_data)

    def test_google_maps_integration_methods(self):
        """Test Google Maps specific methods."""
        business = Business.objects.create(**self.business_data)

        # Test get_google_maps_coordinates
        coords = business.get_google_maps_coordinates()
        self.assertIsNotNone(coords)
        self.assertEqual(coords["lat"], 51.507351)
        self.assertEqual(coords["lng"], -0.127758)

        # Test get_google_maps_url
        url = business.get_google_maps_url()
        self.assertIsNotNone(url)
        self.assertIn("google.com/maps", url)
        self.assertIn("51.507351", url)
        self.assertIn("-0.127758", url)


class BusinessReviewModelTest(TestCase):
    """Test cases for the BusinessReview model."""

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@example.com", password="testpass123"
        )

        self.reviewer = User.objects.create_user(
            username="reviewer", email="reviewer@example.com", password="testpass123"
        )

        self.business = Business.objects.create(
            name="Test Business",
            address="123 Test St",
            postcode="SW1A 1AA",
            city="London",
            business_type="cafe",
            owner=self.owner,
        )

    def test_review_creation(self):
        """Test creating a business review."""
        review = BusinessReview.objects.create(
            business=self.business,
            reviewer=self.reviewer,
            rating="positive",
            comment="Great accessibility features!",
        )

        self.assertEqual(review.business, self.business)
        self.assertEqual(review.reviewer, self.reviewer)
        self.assertEqual(review.rating, "positive")
        self.assertTrue(review.is_approved)

    def test_review_str_representation(self):
        """Test string representation of review."""
        review = BusinessReview.objects.create(
            business=self.business, reviewer=self.reviewer, rating="positive"
        )

        expected = (
            f"Positive review of {self.business.name} by {self.reviewer.username}"
        )
        self.assertEqual(str(review), expected)

    def test_unique_review_per_user_per_business(self):
        """Test that a user can only review a business once."""
        BusinessReview.objects.create(
            business=self.business, reviewer=self.reviewer, rating="positive"
        )

        # Second review should raise IntegrityError due to unique_together
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            BusinessReview.objects.create(
                business=self.business, reviewer=self.reviewer, rating="negative"
            )


class BusinessPhotoModelTest(TestCase):
    """Test cases for the BusinessPhoto model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="user@example.com", password="testpass123"
        )

        self.business = Business.objects.create(
            name="Test Business",
            address="123 Test St",
            postcode="SW1A 1AA",
            city="London",
            business_type="cafe",
            owner=self.user,
        )

    def test_photo_creation(self):
        """Test creating a business photo."""
        # Note: In a real test, you'd want to use a test image file
        photo = BusinessPhoto.objects.create(
            business=self.business,
            photo="test_image.jpg",  # This would be a proper file in production
            photo_type="exterior",
            caption="Front entrance",
            uploaded_by=self.user,
            is_primary=True,
        )

        self.assertEqual(photo.business, self.business)
        self.assertEqual(photo.photo_type, "exterior")
        self.assertTrue(photo.is_primary)
        self.assertEqual(photo.uploaded_by, self.user)

    def test_photo_str_representation(self):
        """Test string representation of photo."""
        photo = BusinessPhoto.objects.create(
            business=self.business,
            photo="test_image.jpg",
            photo_type="interior",
            uploaded_by=self.user,
        )

        expected = f"Interior Photo photo of {self.business.name}"
        self.assertEqual(str(photo), expected)
