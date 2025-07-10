from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Business(models.Model):
    """
    Core Business model for accessibility ratings
    """
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text="Business name")
    description = models.TextField(blank=True, help_text="Business description")
    
    # Contact Information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Location
    address = models.TextField(help_text="Full business address")
    postcode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    what3words = models.CharField(max_length=50, blank=True, help_text="What3Words location")
    
    # Business Categories
    BUSINESS_TYPES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Cafe'),
        ('shop', 'Shop'),
        ('hotel', 'Hotel'),
        ('office', 'Office'),
        ('entertainment', 'Entertainment'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES, default='other')
    
    # Accessibility Rating (1-5)
    ACCESSIBILITY_RATINGS = [
        (1, 'Limited Mobility Friendly'),
        (2, 'Wheelchair Accessible Entry'),
        (3, 'Accessible Bathroom'),
        (4, 'Changing Places Bathroom'),
        (5, 'Fully Accessible Events'),
    ]
    accessibility_rating = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=ACCESSIBILITY_RATINGS,
        help_text="Official accessibility rating (1-5)"
    )
    
    # Assessment Information
    last_assessed = models.DateTimeField(null=True, blank=True)
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessed_businesses')
    assessment_notes = models.TextField(blank=True, help_text="Internal assessment notes")
    
    # Business Management
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_businesses')
    is_verified = models.BooleanField(default=False, help_text="Business ownership verified")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Business is active and accepting customers")
    
    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_business_type_display()})"
    
    @property
    def has_accessibility_rating(self):
        """Check if business has been rated for accessibility"""
        return self.accessibility_rating is not None
    
    @property
    def qr_code_url(self):
        """Generate QR code URL for this business"""
        # We'll implement QR code generation later
        return f"/business/{self.id}/qr/"
    
    @property
    def public_url(self):
        """Public URL for this business"""
        return f"/business/{self.id}/"
