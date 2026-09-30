from django.contrib import admin

from .models import FeaturedGame, Follow, User, UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(FeaturedGame)
