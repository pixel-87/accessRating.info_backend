"""
Tests for the businesses app serializers.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from apps.businesses.models import Business
from apps.businesses.serializers import BusinessSerializer


class BusinessSerializerTest(TestCase):
    """Test cases for BusinessSerializer."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.business_data = {
            'name': 'Test Business',
            'description': 'A test business for accessibility',
            'address': '123 Test Street',
            'postcode': 'SW1A 1AA',
            'city': 'London',
            'latitude': 51.507351,
            'longitude': -0.127758,
            'business_type': 'cafe',
            'accessibility_level': 3,
        }
        
        self.business = Business.objects.create(
            owner=self.user,
            **self.business_data
        )

    def test_business_serialization(self):
        """Test serializing a Business instance."""
        serializer = BusinessSerializer(self.business)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Business')
        self.assertEqual(data['accessibility_level'], 3)
        self.assertEqual(data['business_type'], 'cafe')
        self.assertEqual(data['owner'], 'testuser')
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

    def test_business_deserialization_valid_data(self):
        """Test deserializing valid business data."""
        data = {
            'name': 'New Business',
            'description': 'A new business',
            'address': '456 New Street',
            'postcode': 'W1A 1AA',
            'city': 'London',
            'business_type': 'restaurant',
            'accessibility_level': 2,
        }
        
        serializer = BusinessSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        business = serializer.save(owner=self.user)
        self.assertEqual(business.name, 'New Business')
        self.assertEqual(business.accessibility_level, 2)
        self.assertEqual(business.owner, self.user)

    def test_business_deserialization_invalid_accessibility_level(self):
        """Test deserializing with invalid accessibility level."""
        data = {
            'name': 'Invalid Business',
            'accessibility_level': 6,  # Invalid - should be 1-5
            'business_type': 'cafe',
        }
        
        serializer = BusinessSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('accessibility_level', serializer.errors)

    def test_business_deserialization_invalid_postcode(self):
        """Test deserializing with invalid UK postcode."""
        data = {
            'name': 'Invalid Postcode Business',
            'postcode': 'INVALID',  # Invalid UK postcode format
            'business_type': 'cafe',
        }
        
        serializer = BusinessSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('postcode', serializer.errors)

    def test_business_deserialization_missing_required_fields(self):
        """Test deserializing with missing required fields."""
        data = {
            'description': 'Missing name field',
        }
        
        serializer = BusinessSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_read_only_fields(self):
        """Test that read-only fields cannot be set during creation."""
        data = {
            'name': 'Test Business',
            'owner': 'hacker',  # This should be ignored
            'created_at': '2020-01-01T00:00:00Z',  # This should be ignored
            'business_type': 'cafe',
            'address': '123 Test Street',
            'postcode': 'SW1A 1AA',
            'city': 'London',
        }
        
        serializer = BusinessSerializer(data=data)
        self.assertTrue(serializer.is_valid(), f"Serializer errors: {serializer.errors}")
        
        business = serializer.save(owner=self.user)
        self.assertEqual(business.owner, self.user)  # Should use the owner passed to save()
        self.assertNotEqual(business.created_at.year, 2020)  # Should use current timestamp

    def test_accessibility_level_display(self):
        """Test the accessibility level display field."""
        serializer = BusinessSerializer(self.business)
        data = serializer.data
        
        self.assertIn('accessibility_level_display', data)
        self.assertEqual(
            data['accessibility_level_display'],
            'Rating 3: Includes wheelchair-accessible bathroom with grab bars'
        )

    def test_location_fields(self):
        """Test latitude and longitude fields are included."""
        serializer = BusinessSerializer(self.business)
        data = serializer.data
        
        self.assertIn('latitude', data)
        self.assertIn('longitude', data)
        # Should have default London coordinates
        self.assertEqual(float(data['latitude']), 51.507351)
        self.assertEqual(float(data['longitude']), -0.127758)

    def test_partial_update(self):
        """Test partial update of business data."""
        data = {
            'name': 'Updated Name Only',
        }
        
        serializer = BusinessSerializer(self.business, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_business = serializer.save()
        self.assertEqual(updated_business.name, 'Updated Name Only')
        self.assertEqual(updated_business.business_type, 'cafe')  # Should remain unchanged
