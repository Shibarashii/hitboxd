from django import forms


class GameSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. Hollow Knight...",
            "class": "form-input"
        }),
    )
    page = forms.IntegerField(required=False, min_value=1, widget=forms.HiddenInput)
