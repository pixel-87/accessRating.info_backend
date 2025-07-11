from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile information
    phone_number = models.CharField(
        max_length=15, 
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    
    # Platform-specific settings
    email_notifications = models.BooleanField(default=True, help_text="Receive email notifications")
    location_sharing = models.BooleanField(default=False, help_text="Allow location-based recommendations")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    


class BusinessOwner(models.Model):
    """
    Model for users who own/manage businesses and can update business information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_owner')
    
    # Business owner verification - for now this will be done manually, businesses can just email in proof.
    is_verified = models.BooleanField(default=False, help_text="Owner has been verified")
    verification_document = models.FileField(
        upload_to='verification_docs/', 
        blank=True, 
        null=True,
        help_text="Business registration or ownership proof"
    )
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # Contact information
    business_email = models.EmailField(blank=True, help_text="Primary business contact email")
    business_phone = models.CharField(
        max_length=15, 
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Business Owner"
        verbose_name_plural = "Business Owners"
    
    def __str__(self):
        return f"Business Owner: {self.user.username}"
    
    @property
    def owned_businesses_count(self):
        """Return count of businesses owned by this user."""
        return self.user.businesses.count()


class AccessibilityAssessor(models.Model):
    """
    Model for certified accessibility assessor who can conduct official assessments.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accessibility_assessor')
    
    # Professional information
    bio = models.TextField(blank=True, help_text="Professional background and expertise")
    linkedin_profile = models.URLField(blank=True)
    
    # Platform status
    is_active = models.BooleanField(default=True, help_text="Can conduct assessments")
    is_approved = models.BooleanField(default=False, help_text="Approved by platform admin")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Accessibility Assessor"
        verbose_name_plural = "Accessibility Assessors"

    def __str__(self):
        return f"Assessor: {self.user.username}"

    @property
    def is_certification_valid(self):
        """Check if certification is still valid."""
        from django.utils import timezone
        return self.certification_expiry > timezone.now().date()
    
    @property
    def assessments_count(self):
        """Return count of assessments conducted."""
        return self.user.conducted_assessments.count() if hasattr(self.user, 'conducted_assessments') else 0

# Signal to create UserProfile automatically when User is created

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
