from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User

# class SignUpForm(forms.Form):
#     email = forms.EmailField(
#         max_length=50, widget=forms.EmailInput(attrs={"class": "form-input"})
#     )
#     username = forms.CharField(
#         max_length=50, widget=forms.TextInput(attrs={"class": "form-input"})
#     )
#     password = forms.CharField(
#         max_length=50, widget=forms.PasswordInput(attrs={"class": "form-input"})
#     )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email"]
