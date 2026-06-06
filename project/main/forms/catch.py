from decimal import Decimal
from django import forms
from django.forms import inlineformset_factory

from ..models import FishingTrip, Catch, CatchPhoto


class CatchForm(forms.ModelForm):
    weight = forms.DecimalField(
        min_value=Decimal("0.01"),
        decimal_places=2,
        required=False,
        help_text="Weight of this fish in kg",
    )

    class Meta:
        model = Catch
        fields = ["fish_type", "weight"]


CatchFormSet = inlineformset_factory(
    FishingTrip,
    Catch,
    form=CatchForm,
    can_delete=True,
    extra=0,
    max_num=100,
    validate_max=True,
)


CatchPhotoFormSet = inlineformset_factory(
    Catch,
    CatchPhoto,
    fields=["photo", "caption"],
    can_delete=True,
    extra=1,
    max_num=10,
    validate_max=True,
)
