from django import forms
from django.core.validators import RegexValidator

from ..models import FishType

fish_name_validator = RegexValidator(
    regex=r"^[A-Za-zА-Яа-яІіЇїЄєҐґ\s\-]+$",
    message="Fish name can contain only letters, spaces, and hyphens.",
)


class FishTypeForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="Fish Type Name",
        validators=[fish_name_validator],
        widget=forms.TextInput(attrs={"placeholder": "Enter fish type"}),
    )

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not any(c.isalpha() for c in name):
            raise forms.ValidationError("Fish name must contain at least one letter.")
        return name

    class Meta:
        model = FishType
        fields = ["name"]
