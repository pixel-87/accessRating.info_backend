"""
Business models for the accessibility rating system.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Business(models.Model):
    """
    Model representing a business that can be rated for accessibility.
    Based on the Access Rating Scheme requirements.
    """
    
    # Accessibility rating choices based on the documentation
    ACCESSIBILITY_CHOICES = [
        (1, 'Rating 1: Accessible to individuals with limited mobility'),
        (2, 'Rating 2: Accessible to wheelchair users with step-free entry'),
        (3, 'Rating 3: Includes wheelchair-accessible bathroom with grab bars'),
        (4, 'Rating 4: Includes "Changing Places" bathroom with hoist system'),
        (5, 'Rating 5: Fully accessible for multiple users with diverse needs'),
    ]
    
    # Business type choices
    BUSINESS_TYPE_CHOICES = [
        ('cafe', 'Cafe'),
        ('restaurant', 'Restaurant'),
        ('shop', 'Shop'),
        ('pub', 'Pub'),
        ('hotel', 'Hotel'),
        ('office', 'Office'),
        ('healthcare', 'Healthcare'),
        ('entertainment', 'Entertainment'),
        ('education', 'Education'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ]
    
    # Primary key - using AutoField as per requirements (ID - Int(short), Autoincrement, PK)
    id = models.AutoField(primary_key=True)
    
    # Basic business information - BusinessName - String
    name = models.CharField(max_length=200, help_text="Business name")
    
    # BusinessDescription - String (100 word limit) - editable by business account
    description = models.TextField(
        max_length=600,  # Roughly 100 words
        blank=True, 
        help_text="Business description (editable by business owner, ~100 words)"
    )
    
    # Address - String (with postcode validation)
    address = models.TextField(help_text="Full address of the business")
    postcode = models.CharField(
        max_length=10, 
        help_text="UK postcode",
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}$',
                message='Enter a valid UK postcode (e.g., SW1A 1AA)',
                flags=0
            )
        ]
    )
    city = models.CharField(max_length=100, default='', help_text="City")
    
    # Location - Optimized for Google Maps integration
    latitude = models.DecimalField(
        max_digits=12,  # High precision for exact positioning (centimeter accuracy)
        decimal_places=9,
        default='51.507351',  # London center as default for UK businesses
        help_text="Latitude coordinate for Google Maps (required for map display)"
    )
    longitude = models.DecimalField(
        max_digits=12,  # High precision for exact positioning 
        decimal_places=9,
        default='-0.127758',  # London center as default for UK businesses
        help_text="Longitude coordinate for Google Maps (required for map display)"
    )
    
    # BusinessType + specialisation
    business_type = models.CharField(
        max_length=50,
        choices=BUSINESS_TYPE_CHOICES,
        default='other',
        help_text="Type of business (e.g., cafe, restaurant, shop)"
    )
    specialisation = models.CharField(
        max_length=100,
        blank=True,
        help_text="Business specialisation (e.g., 'Italian' for restaurant)"
    )
    
    # ContactInfo - business contact info (email or phone)
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    email = models.EmailField(blank=True, help_text="Contact email")
    website = models.URLField(blank=True, help_text="Business website")
    
    # Opening times
    opening_times = models.TextField(
        blank=True,
        help_text="Business opening times (editable by business owner)"
    )
    
    # AccessibilityRating - The rating from 1-5 made by volunteer, then approved
    accessibility_level = models.IntegerField(
        choices=ACCESSIBILITY_CHOICES,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Accessibility rating (1-5) assigned by trained volunteer assessor"
    )
    
    # AccessibilityFeatures - specific notes (e.g., "go to side window and ask for ramp")
    # Editable by business account
    accessibility_features = models.TextField(
        blank=True,
        help_text="Specific accessibility notes and features (editable by business owner)"
    )
    
    # Additional accessibility barriers or limitations
    accessibility_barriers = models.TextField(
        blank=True,
        help_text="Description of accessibility barriers or limitations"
    )
    
    # AccessReport - Full report of how accessible it is
    access_report = models.TextField(
        blank=True,
        help_text="Full accessibility assessment report provided with rating"
    )
    
    # Assessment dates
    # FirstAssessedDate - Date the business was first assessed
    first_assessed_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when business was first assessed"
    )
    
    # NextAssessmentDate - Date of next assessment (automatic or scheduled)
    next_assessment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Scheduled date for next assessment (every 3 years or on request)"
    )
    
    # Ownership and management
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='businesses',
        null=True,  # Temporarily nullable for migration
        blank=True,
        help_text="User who added/owns this business listing (business account)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional metadata
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether this business listing has been verified by an admin"
    )
    
    # Sticker information
    sticker_requested = models.BooleanField(
        default=False,
        help_text="Whether business has requested stickers"
    )
    
    sticker_type = models.CharField(
        max_length=20,
        choices=[
            ('window_inside', 'Window (sticky on image side)'),
            ('window_outside', 'Window (sticky on back side)'),
        ],
        blank=True,
        help_text="Type of sticker requested"
    )
    
    # Business notes/requests (e.g., "please book in advance")
    business_notes = models.TextField(
        blank=True,
        help_text="Business notes and special requests (e.g., call in advance, bookings required)"
    )
    
    # Special mentions (e.g., employs people with learning disabilities)
    special_mentions = models.TextField(
        blank=True,
        help_text="Special mentions about the business (e.g., employs people with disabilities)"
    )
    
    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['postcode']),
            models.Index(fields=['city']),
            models.Index(fields=['business_type']),
            models.Index(fields=['accessibility_level']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['first_assessed_date']),
            models.Index(fields=['next_assessment_date']),
        ]
    
    def __str__(self):
        """String representation of the business."""
        return f"{self.name} - {self.city}"
    
    def get_full_business_type(self):
        """Return business type with specialisation if available."""
        if self.specialisation:
            return f"{self.specialisation} {self.get_business_type_display()}"
        return self.get_business_type_display()
    
    @property
    def accessibility_level_display(self):
        """Get the display name for accessibility level."""
        return dict(self.ACCESSIBILITY_CHOICES).get(self.accessibility_level, 'Not rated')
    
    @property
    def is_accessible(self):
        """Check if business has good accessibility (rating >= 3)."""
        return self.accessibility_level and self.accessibility_level >= 3
    
    @property
    def needs_reassessment(self):
        """Check if business needs reassessment (3 years have passed)."""
        if not self.first_assessed_date or not self.next_assessment_date:
            return False
        from django.utils import timezone
        return timezone.now().date() >= self.next_assessment_date.date()
    
    def generate_qr_code_data(self):
        """Generate data for QR code (business ID and name)."""
        return f"business_id_{self.id}_{self.name.replace(' ', '_')}"
    
    @property
    def has_location_data(self):
        """Check if business has lat/lng coordinates for Google Maps."""
        return self.latitude is not None and self.longitude is not None
    
    def get_google_maps_coordinates(self):
        """Get coordinates formatted for Google Maps API."""
        if self.has_location_data:
            return {
                'lat': float(self.latitude),
                'lng': float(self.longitude)
            }
        return None
    
    def get_google_maps_url(self):
        """Generate Google Maps URL for this business location."""
        if self.has_location_data:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return None


class BusinessReview(models.Model):
    """
    Model for eBay-style reviews of businesses.
    Users can add positive, neutral, or negative ratings with comments and photos.
    """
    
    REVIEW_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]
    
    # Link to business and reviewer
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text="Business being reviewed"
    )
    
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='business_reviews',
        help_text="User who wrote the review"
    )
    
    # Review content
    rating = models.CharField(
        max_length=10,
        choices=REVIEW_CHOICES,
        help_text="Overall experience rating (required if other fields are added)"
    )
    
    comment = models.TextField(
        blank=True,
        help_text="User's comment about their experience"
    )
    
    # Photo upload (will need proper file handling in production)
    photo = models.ImageField(
        upload_to='business_reviews/',
        blank=True,
        null=True,
        help_text="Photo of the business experience"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Moderation
    is_approved = models.BooleanField(
        default=True,
        help_text="Whether this review has been approved by moderators"
    )
    
    class Meta:
        verbose_name = "Business Review"
        verbose_name_plural = "Business Reviews"
        ordering = ['-created_at']
        # Prevent multiple reviews from same user for same business
        unique_together = ['business', 'reviewer']
        indexes = [
            models.Index(fields=['business', '-created_at']),
            models.Index(fields=['rating']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self):
        """String representation of the review."""
        return f"{self.get_rating_display()} review of {self.business.name} by {self.reviewer.username}"


class BusinessPhoto(models.Model):
    """
    Model for storing business photos (outside and inside).
    """
    
    PHOTO_TYPE_CHOICES = [
        ('exterior', 'Exterior Photo'),
        ('interior', 'Interior Photo'),
        ('accessibility', 'Accessibility Feature'),
        ('entrance', 'Entrance'),
        ('facilities', 'Facilities'),
    ]
    
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='photos',
        help_text="Business this photo belongs to"
    )
    
    photo = models.ImageField(
        upload_to='business_photos/',
        help_text="Business photo"
    )
    
    photo_type = models.CharField(
        max_length=20,
        choices=PHOTO_TYPE_CHOICES,
        help_text="Type of photo"
    )
    
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Photo caption or description"
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text="User who uploaded this photo"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_primary = models.BooleanField(
        default=False,
        help_text="Whether this is the primary photo for the business"
    )
    
    class Meta:
        verbose_name = "Business Photo"
        verbose_name_plural = "Business Photos"
        ordering = ['-is_primary', '-created_at']
        indexes = [
            models.Index(fields=['business', '-created_at']),
            models.Index(fields=['photo_type']),
            models.Index(fields=['is_primary']),
        ]
    
    def __str__(self):
        """String representation of the photo."""
        return f"{self.get_photo_type_display()} photo of {self.business.name}"
