from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserFavorite, UserProfile, UserSearchHistory


class UserProfileInline(admin.StackedInline):
    """Inline admin for user profile"""

    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fields = [
        "user_type",
        "phone",
        "bio",
        "accessibility_needs",
        "business_license_number",
        "assessor_training_completed",
        "assessor_certification_date",
        "email_notifications",
        "profile_public",
    ]


class CustomUserAdmin(UserAdmin):
    """Extended user admin with profile inline"""

    inlines = (UserProfileInline,)

    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "get_user_type",
        "is_active",
        "date_joined",
    ]

    list_filter = UserAdmin.list_filter + ("profile__user_type",)

    def get_user_type(self, obj):
        """Get user type from profile"""
        try:
            return obj.profile.get_user_type_display()
        except UserProfile.DoesNotExist:
            return "No Profile"

    get_user_type.short_description = "User Type"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for user profiles"""

    list_display = [
        "user",
        "user_type",
        "phone",
        "assessor_training_completed",
        "profile_public",
        "created_at",
    ]
    list_filter = ["user_type", "assessor_training_completed", "profile_public"]
    search_fields = ["user__username", "user__email", "phone"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    """Admin for user favorites"""

    list_display = ["user", "business", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "business__name"]
    readonly_fields = ["created_at"]


@admin.register(UserSearchHistory)
class UserSearchHistoryAdmin(admin.ModelAdmin):
    """Admin for user search history"""

    list_display = [
        "user",
        "search_query",
        "search_location",
        "business_type_filter",
        "accessibility_filter",
        "created_at",
    ]
    list_filter = ["business_type_filter", "accessibility_filter", "created_at"]
    search_fields = ["user__username", "search_query", "search_location"]
    readonly_fields = ["created_at"]


# Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
