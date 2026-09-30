from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="following_set"
    )
    following = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="follower_set"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [  
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow"
            )
        ]


class FeaturedGames(models.Model):
    pass
