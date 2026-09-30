from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s Profile'"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following_set"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower_set"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.follower.username} follows {self.following.username}"


class FeaturedGame(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="featured_games"
    )
    game = models.ForeignKey(
        "games.Game", on_delete=models.CASCADE, related_name="featured_by"
    )
    position = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "position"], name="unique_featured_position"
            ),
            models.UniqueConstraint(
                fields=["user", "game"], name="unique_featured_game"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - #{self.position} {self.game.name}"
