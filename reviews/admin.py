from django.contrib import admin
from .models import LogEntry, Review

# Register your models here.
admin.site.register(LogEntry)
admin.site.register(Review)

