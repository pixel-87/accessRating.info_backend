from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # User profile management
    path("profile/", views.UserProfileView.as_view(), name="user-profile"),
    path("stats/", views.user_stats, name="user-stats"),
    path("update-type/", views.update_user_type, name="update-user-type"),
    # Favorites management
    path(
        "favorites/",
        views.UserFavoritesListView.as_view(),
        name="user-favorites-list",
    ),
    path(
        "favorites/<int:pk>/",
        views.UserFavoriteDetailView.as_view(),
        name="user-favorite-detail",
    ),
    path(
        "favorites/toggle/<int:business_id>/",
        views.toggle_favorite,
        name="toggle-favorite",
    ),
    # Search history
    path(
        "search-history/",
        views.UserSearchHistoryView.as_view(),
        name="user-search-history",
    ),
]
