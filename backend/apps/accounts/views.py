from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserFavorite, UserProfile, UserSearchHistory
from .serializers import (
    UserFavoriteSerializer,
    UserSearchHistorySerializer,
    UserUpdateSerializer,
)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user's profile"""

    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserFavoritesListView(generics.ListCreateAPIView):
    """List and create user favorites"""

    serializer_class = UserFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFavorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserFavoriteDetailView(generics.DestroyAPIView):
    """Remove a favorite"""

    serializer_class = UserFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFavorite.objects.filter(user=self.request.user)


class UserSearchHistoryView(generics.ListCreateAPIView):
    """List and create user search history"""

    serializer_class = UserSearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSearchHistory.objects.filter(user=self.request.user)[
            :20
        ]  # Last 20 searches

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, business_id):
    """Toggle favorite status for a business"""

    user = request.user

    try:
        from apps.businesses.models import Business

        business = get_object_or_404(Business, id=business_id)

        favorite, created = UserFavorite.objects.get_or_create(
            user=user, business=business
        )

        if not created:
            # Favorite exists, remove it
            favorite.delete()
            return Response(
                {
                    "favorited": False,
                    "message": f"Removed {business.name} from favorites",
                }
            )
        else:
            # Favorite created
            return Response(
                {
                    "favorited": True,
                    "message": f"Added {business.name} to favorites",
                }
            )

    except Exception:
        return Response(
            {"error": "Unable to toggle favorite"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """Get user statistics"""

    user = request.user

    # Get or create profile
    profile, created = UserProfile.objects.get_or_create(user=user)

    stats = {
        "user_type": profile.user_type,
        "businesses_owned": user.businesses.count(),
        "favorites_count": user.favorites.count(),
        "reviews_count": user.business_reviews.count(),
        "photos_uploaded": user.businessphoto_set.count(),
        "can_assess_businesses": profile.can_assess_businesses,
        "member_since": user.date_joined.strftime("%Y-%m-%d"),
    }

    return Response(stats)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user_type(request):
    """Update user type (e.g., regular to business owner)"""

    user_type = request.data.get("user_type")

    if user_type not in ["regular", "business", "assessor"]:
        return Response(
            {"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Get or create profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.user_type = user_type
    profile.save()

    return Response(
        {
            "message": f"User type updated to {user_type}",
            "user_type": profile.get_user_type_display(),
        }
    )
