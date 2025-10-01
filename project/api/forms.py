import datetime

from django import forms
from django.forms import inlineformset_factory
from .models import FishingTrip, Catch


class CatchForm(forms.ModelForm):
    class Meta:
        model = Catch
        fields = ["fish_type", "weight", "photo"]


CatchFormSet = inlineformset_factory(
    FishingTrip,
    Catch,
    form=CatchForm,
    extra=1,
    can_delete=True,
)


class FishingTripForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        required=True,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date", "max": datetime.date.today().isoformat()},
        ),
    )

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future.")
        return date

    class Meta:
        model = FishingTrip
        fields = ["country_code", "date"]
