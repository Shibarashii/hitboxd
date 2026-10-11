from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from .models import User


# Create your views here.
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    queryset = User.objects.select_related("profile")
    template_name = "users/profile.html"
    context_object_name = "user_profile"
    slug_field = "username"
    slug_url_kwarg = "username"
    



