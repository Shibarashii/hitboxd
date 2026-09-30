from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Status(models.TextChoices):
    PLAYED = "played", "Played"
    PLAYING = "playing", "Playing"
    WANT_TO_PLAY = "want", "Want to Play"

class LogEntry(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="log_entries"
    )
    game = models.ForeignKey(
        "games.Game", on_delete=models.CASCADE, related_name="logged_by"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLAYED)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"], name="unique_user_game_log"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.game.name} ({self.get_status_display()})"


class Review(models.Model):
    log_entry = models.OneToOneField(
        LogEntry, on_delete=models.CASCADE, related_name="review"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"Review by {self.log_entry.user.username} on {self.log_entry.game.name}" 
