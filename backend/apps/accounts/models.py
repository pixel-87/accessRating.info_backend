from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class UserProfile(models.Model):
    """Extended user profile for additional user information"""

    USER_TYPE_CHOICES = [
        ("regular", "Regular User"),
        ("business", "Business Owner"),
        ("assessor", "Volunteer Assessor"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="Associated Django user account",
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default="regular",
        help_text="Type of user account",
    )

    # Contact information
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message=(
                    "Phone number must be entered in the format: "
                    "+999999999'. Up to 15 digits allowed."
                ),
            )
        ],
        help_text="Contact phone number",
    )

    # Profile information
    bio = models.TextField(
        max_length=500, blank=True, help_text="User biography or description"
    )

    # Accessibility preferences for regular users
    accessibility_needs = models.TextField(
        blank=True,
        help_text="User's accessibility requirements and preferences",
    )

    # Business-specific information
    business_license_number = models.CharField(
        max_length=50,
        blank=True,
        help_text=(
            "Business license or registration number (for business accounts)"
        ),
    )

    # Assessor-specific information
    assessor_training_completed = models.BooleanField(
        default=False, help_text="Whether assessor has completed training"
    )
    assessor_certification_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when assessor completed certification",
    )

    # Privacy settings
    email_notifications = models.BooleanField(
        default=True, help_text="Receive email notifications"
    )

    profile_public = models.BooleanField(
        default=False, help_text="Make profile visible to other users"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

    @property
    def is_business_owner(self):
        """Check if user is a business owner"""
        return self.user_type == "business"

    @property
    def is_assessor(self):
        """Check if user is a volunteer assessor"""
        return self.user_type == "assessor"

    @property
    def can_assess_businesses(self):
        """Check if user can assess businesses"""
        return self.is_assessor and self.assessor_training_completed


class UserFavorite(models.Model):
    """User's favorite businesses"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        help_text="User who favorited the business",
    )

    business = models.ForeignKey(
        "businesses.Business",
        on_delete=models.CASCADE,
        related_name="favorited_by",
        help_text="The favorited business",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "business"]
        verbose_name = "User Favorite"
        verbose_name_plural = "User Favorites"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} favorited {self.business.name}"


class UserSearchHistory(models.Model):
    """Track user search history for better recommendations"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="search_history",
        help_text="User who performed the search",
    )

    search_query = models.CharField(
        max_length=200,
        help_text="The search query",
    )

    search_location = models.CharField(
        max_length=200, blank=True, help_text="Location used in search"
    )

    business_type_filter = models.CharField(
        max_length=50, blank=True, help_text="Business type filter applied"
    )

    accessibility_filter = models.IntegerField(
        null=True, blank=True, help_text="Minimum accessibility level filter"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Search History"
        verbose_name_plural = "User Search Histories"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} searched for '{self.search_query}'"
