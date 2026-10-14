from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import LogEntry
from games.models import Game


# Create your views here.
class RateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        game = get_object_or_404(Game, slug=slug)
        rating = request.POST.get("rating")

        if rating not in {"1", "2", "3", "4", "5"}:
            return HttpResponseBadRequest("Rating must be 1-5")
        LogEntry.objects.update_or_create(
            user=request.user,
            game=game,
            defaults={"rating": int(rating)}
        )
        return redirect("game-details", slug=slug)
