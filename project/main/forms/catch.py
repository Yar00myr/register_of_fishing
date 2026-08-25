from django import forms
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput
from decimal import Decimal
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


class CatchPhotoForm(forms.ModelForm):
    class Meta:
        model = CatchPhoto
        fields = ["photo", "caption"]
        widgets = {
            "photo": ClearableFileInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].widget.show_hidden_initial = False
        self.fields["photo"].widget.template_name = "django/forms/widgets/file.html"


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
    form=CatchPhotoForm,
    can_delete=True,
    extra=1,
    max_num=10,
    validate_max=True,
)
