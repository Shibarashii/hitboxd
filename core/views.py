from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from users.models import User

from .forms import SignUpForm


class HomePageView(TemplateView):
    template_name = "core/homepage.html"

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "core/signup.html"
    success_url = "core/homepage.html"
