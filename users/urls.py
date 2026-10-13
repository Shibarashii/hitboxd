from django.urls import path

from . import views

urlpatterns = [
    path("", views.MemberListView.as_view(), name="member-list"),
    path(
        "<str:username>",
        views.UserProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    path("settings/profile/", views.EditUserProfileView.as_view(), name="update-profile")
]
