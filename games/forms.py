from django import forms


class GameSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. Hollow Knight...",
            "class": "border rounded px-3 py-2 w-full",
        }),
    )
