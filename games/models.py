from django.db import models


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True)
    rawg_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Game(models.Model):
    rawg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    cover_url = models.URLField(blank=True)
    first_release_date = models.DateField(null=True, blank=True)
    summary = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name="games", blank=True)

    def __str__(self) -> str:
        return self.name
