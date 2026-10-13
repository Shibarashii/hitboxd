from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "avatar_url"]
        labels = {"avatar_url" : "Avatar"}
        widgets = {"avatar_url": forms.FileInput}

