from django import forms


class GameSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. Hollow Knight...",
            "class": "form-input"
        }),
    )
