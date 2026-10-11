from django.urls import path

from . import views

urlpatterns = [
    path(
        "<str:username>",
        views.UserProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    path("", views.MemberListView.as_view(), name="member-list"),
]
