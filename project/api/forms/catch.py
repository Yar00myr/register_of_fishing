import datetime

from django import forms
from django.forms import inlineformset_factory
from ..models import FishingTrip, Catch


class CatchForm(forms.ModelForm):
    weight = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        required=False,
        help_text="weight in kg",
        widget=forms.NumberInput(),
    )

    def clean_weight(self):
        weight = self.cleaned_data["weight"]
        if weight is None:
            return None

        if weight <= 0:
            raise forms.ValidationError("The weight must be greater than 0 kg.")
        else:
            return weight

    class Meta:
        model = Catch
        fields = ["fish_type", "weight", "photo"]


CatchFormSet = inlineformset_factory(
    FishingTrip,
    Catch,
    form=CatchForm,
    can_delete=False,
)
