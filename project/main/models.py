import json
import os

from django.db import models

COUNTRIES_FILE = os.path.join(os.path.dirname(__file__), "data/country.json")

with open(COUNTRIES_FILE, encoding="utf-8") as f:
    _countries_data = json.load(f)

COUNTRY_CHOICES = [(c["code"], c["name"]) for c in _countries_data]
_COUNTRY_MAP = {c["code"]: c["name"] for c in _countries_data}


def catch_photo_upload_path(instance: "CatchPhoto", filename: str) -> str:
    return f"catches/{instance.catch_id}/{filename}"


class FishingTrip(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    country_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default="UA")
    date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Fishing trip"
        verbose_name_plural = "Fishing trips"

    @property
    def country_name(self) -> str:
        return _COUNTRY_MAP.get(self.country_code, self.country_code)

    def __str__(self) -> str:
        label = self.name or self.country_name
        return f"Fishing trip — {label} ({self.date})"


class FishType(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Fish type"
        verbose_name_plural = "Fish types"

    def __str__(self) -> str:
        return self.name


class Catch(models.Model):
    fishing_trip = models.ForeignKey(
        FishingTrip, on_delete=models.CASCADE, related_name="catches"
    )
    fish_type = models.ForeignKey(
        FishType, on_delete=models.CASCADE, related_name="catches"
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Weight of this fish in kg",
    )

    def __str__(self):
        if self.weight:
            return f"{self.fish_type} ({self.weight} kg)"
        return str(self.fish_type)


class CatchPhoto(models.Model):
    catch = models.ForeignKey(Catch, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to=catch_photo_upload_path)
    caption = models.CharField(max_length=200, blank=True, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["uploaded_at"]
