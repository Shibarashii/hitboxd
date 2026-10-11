from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from users.models import User

from .forms import SignUpForm


class HomePageView(TemplateView):
    template_name = "core/homepage.html"

class SignUpView(SuccessMessageMixin,CreateView):
    model = User
    form_class = SignUpForm
    template_name = "core/registration.html"
    success_url = reverse_lazy("homepage")
    success_message = "Account created."

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        if request.user.is_authenticated:
            return redirect("homepage")
        return super().dispatch(request, *args, **kwargs)

