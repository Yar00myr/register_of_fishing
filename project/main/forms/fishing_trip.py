from datetime import date

from django import forms

from ..models import FishingTrip


class FishingTripForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        required=True,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date", "max": date.today().isoformat()},
        ),
    )

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date > date.today():
            raise forms.ValidationError("The date cannot be in the future.")
        return date

    class Meta:
        model = FishingTrip
        fields = ["country_code", "date"]
