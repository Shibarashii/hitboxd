from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Prefetch
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from reviews.models import LogEntry

from .forms import UserProfileForm
from .models import FeaturedGame, User


# Create your views here.
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    queryset = (
        User.objects.select_related("profile")
        .prefetch_related(
            Prefetch("featured_games", queryset=FeaturedGame.objects.select_related("game"))
        )
        .prefetch_related(
            Prefetch(
                "log_entries",
                queryset=LogEntry.objects.select_related("review", "game"),
            )
        )
        .annotate(
            follower_count=Count("follower_set", distinct=True),
            following_count=Count("following_set", distinct=True),
            review_count=Count("log_entries__review", distinct=True),
        )
    )
    template_name = "users/profile.html"
    context_object_name = "member"
    slug_field = "username"
    slug_url_kwarg = "username"


class MemberListView(LoginRequiredMixin, ListView):
    model = User
    queryset = User.objects.select_related("profile").annotate(
        follower_count=Count("follower_set", distinct=True),
        review_count=Count("log_entries__review", distinct=True),
    )
    context_object_name = "members"
    template_name = "users/members.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data()
        context["following"] = User.objects.filter(
            follower_set__follower=self.request.user
        ).select_related("profile")

        context["follower"] = User.objects.filter(
            following_set__following=self.request.user
        ).select_related("profile")
        return context


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = "users/update-profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self) -> str:
        return reverse("user-profile-detail", args=[self.request.user.username])
