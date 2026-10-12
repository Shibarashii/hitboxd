from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import User


# Create your views here.
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    queryset = User.objects.select_related("profile")
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
