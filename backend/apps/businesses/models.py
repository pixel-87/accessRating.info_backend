from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone


class Business(models.Model):
    """Business model representing a local business with accessibility information"""
    
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
    
    ACCESSIBILITY_RATING_CHOICES = [
        (1, 'Rating 1: Accessible to individuals with limited mobility'),
        (2, 'Rating 2: Accessible to wheelchair users with step-free entry'),
        (3, 'Rating 3: Includes wheelchair-accessible bathroom with grab bars'),
        (4, 'Rating 4: Includes "Changing Places" bathroom with hoist system'),
        (5, 'Rating 5: Fully accessible for multiple users with diverse needs'),
    ]
    
    STICKER_TYPE_CHOICES = [
        ('window_inside', 'Window (sticky on image side)'),
        ('window_outside', 'Window (sticky on back side)'),
    ]
    
    # Basic business information
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, help_text="Business name")
    description = models.TextField(
        max_length=600, 
        blank=True, 
        help_text="Business description (editable by business owner, ~100 words)"
    )
    
    # Location information
    address = models.TextField(help_text="Full address of the business")
    postcode = models.CharField(
        max_length=10, 
        help_text="UK postcode",
        validators=[RegexValidator(
            regex=r'^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}$',
            message='Enter a valid UK postcode (e.g., SW1A 1AA)'
        )]
    )
    city = models.CharField(max_length=100, default='', help_text="City")
    latitude = models.DecimalField(
        max_digits=10, decimal_places=6, 
        null=True, blank=True, 
        help_text="Latitude for map location"
    )
    longitude = models.DecimalField(
        max_digits=10, decimal_places=6, 
        null=True, blank=True, 
        help_text="Longitude for map location"
    )
    
    # Business details
    business_type = models.CharField(
        max_length=50, 
        choices=BUSINESS_TYPE_CHOICES, 
        default='other',
        help_text="Type of business (e.g., cafe, restaurant, shop)"
    )
    specialisation = models.CharField(
        max_length=100, blank=True, 
        help_text="Business specialisation (e.g., 'Italian' for restaurant)"
    )
    
    # Contact information
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    email = models.EmailField(blank=True, help_text="Contact email")
    website = models.URLField(blank=True, help_text="Business website")
    opening_times = models.TextField(
        blank=True, 
        help_text="Business opening times (editable by business owner)"
    )
    
    # Accessibility information
    accessibility_level = models.IntegerField(
        choices=ACCESSIBILITY_RATING_CHOICES,
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Accessibility rating (1-5) assigned by trained volunteer assessor"
    )
    accessibility_features = models.TextField(
        blank=True, 
        help_text="Specific accessibility notes and features (editable by business owner)"
    )
    accessibility_barriers = models.TextField(
        blank=True, 
        help_text="Description of accessibility barriers or limitations"
    )
    access_report = models.TextField(
        blank=True, 
        help_text="Full accessibility assessment report provided with rating"
    )
    
    # Assessment dates
    first_assessed_date = models.DateTimeField(
        null=True, blank=True, 
        help_text="Date when business was first assessed"
    )
    next_assessment_date = models.DateTimeField(
        null=True, blank=True, 
        help_text="Scheduled date for next assessment (every 3 years or on request)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(
        default=False, 
        help_text="Whether this business listing has been verified by an admin"
    )
    
    # Sticker program
    sticker_requested = models.BooleanField(
        default=False, 
        help_text="Whether business has requested stickers"
    )
    sticker_type = models.CharField(
        max_length=20, 
        choices=STICKER_TYPE_CHOICES, 
        blank=True,
        help_text="Type of sticker requested"
    )
    
    # Additional notes
    business_notes = models.TextField(
        blank=True, 
        help_text="Business notes and special requests (e.g., call in advance, bookings required)"
    )
    special_mentions = models.TextField(
        blank=True, 
        help_text="Special mentions about the business (e.g., employs people with disabilities)"
    )
    
    # Relationships
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='businesses',
        null=True, blank=True,
        help_text="User who added/owns this business listing (business account)"
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
        return f"{self.name} - {self.city}"
    
    # Properties and methods expected by tests
    @property
    def accessibility_level_display(self):
        """Get the display text for accessibility level"""
        if self.accessibility_level:
            return self.get_accessibility_level_display()
        return 'Not rated'
    
    @property
    def is_accessible(self):
        """Check if business has accessibility rating of 3 or higher"""
        return self.accessibility_level is not None and self.accessibility_level >= 3
    
    @property
    def has_location_data(self):
        """Check if business has location coordinates"""
        return self.latitude is not None and self.longitude is not None
    
    @property
    def needs_reassessment(self):
        """Check if business needs reassessment"""
        if self.next_assessment_date:
            return self.next_assessment_date < timezone.now()
        return False
    
    def get_full_business_type(self):
        """Get business type with specialisation if available"""
        if self.specialisation:
            return f"{self.specialisation} {self.get_business_type_display()}"
        return self.get_business_type_display()
    
    def generate_qr_code_data(self):
        """Generate QR code data for the business"""
        # Format expected by tests: business_id_{id}_Test_Cafe_etc
        clean_name = self.name.replace(' ', '_')
        return f"business_id_{self.id}_{clean_name}_{self.city}_{self.accessibility_level}"
    
    def generate_qr_code_url(self):
        """Generate the URL that the QR code should link to"""
        # This will link to the frontend business detail page
        return f"https://yourdomain.com/business/{self.id}"
    
    def generate_qr_code_image(self, base_url="https://yourdomain.com"):
        """Generate actual QR code image"""
        import qrcode
        from io import BytesIO
        
        # Create QR code linking to business detail page
        url = f"{base_url}/business/{self.id}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes for storage/response
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer
    
    def get_google_maps_coordinates(self):
        """Get coordinates formatted for Google Maps"""
        if self.has_location_data:
            return {
                'lat': float(self.latitude),
                'lng': float(self.longitude)
            }
        return None
    
    def get_google_maps_url(self):
        """Get Google Maps URL for the business location"""
        if self.has_location_data:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return None


class BusinessPhoto(models.Model):
    """Photos associated with businesses"""
    
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
        max_length=200, blank=True, 
        help_text="Photo caption or description"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(
        default=False, 
        help_text="Whether this is the primary photo for the business"
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        help_text="User who uploaded this photo"
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
        return f"{self.get_photo_type_display()} photo of {self.business.name}"


class BusinessReview(models.Model):
    """User reviews of businesses"""
    
    RATING_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]
    
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
    rating = models.CharField(
        max_length=10, 
        choices=RATING_CHOICES,
        help_text="Overall experience rating (required if other fields are added)"
    )
    comment = models.TextField(
        blank=True, 
        help_text="User's comment about their experience"
    )
    photo = models.ImageField(
        upload_to='business_reviews/', 
        null=True, blank=True,
        help_text="Photo of the business experience"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(
        default=True, 
        help_text="Whether this review has been approved by moderators"
    )
    
    class Meta:
        verbose_name = "Business Review"
        verbose_name_plural = "Business Reviews"
        ordering = ['-created_at']
        unique_together = ('business', 'reviewer')
        indexes = [
            models.Index(fields=['business', '-created_at']),
            models.Index(fields=['rating']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self):
        return f"{self.get_rating_display()} review of {self.business.name} by {self.reviewer.username}"
