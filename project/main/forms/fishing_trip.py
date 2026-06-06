from datetime import date as date_type
from django import forms

from ..models import FishingTrip


class FishingTripForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        required=True,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date", "max": date_type.today().isoformat()},
        ),
    )

    def clean_date(self):
        value = self.cleaned_data["date"]
        if value > date_type.today():
            raise forms.ValidationError("The date cannot be in the future.")
        return value

    class Meta:
        model = FishingTrip
        fields = ["name", "country_code", "date"]
