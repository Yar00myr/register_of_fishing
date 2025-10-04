from django import forms

from ..models import FishType


class FishTypeForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        label="Fish Type Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter fish type"}
        ),
    )

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("The name of the fish species cannot be empty.")
        return name

    class Meta:
        model = FishType
        fields = ["name"]
