import json
import os

from decimal import Decimal
from django.db import models
from django.db.models import F, DecimalField, Sum

COUNTRIES_FILE = os.path.join(os.path.dirname(__file__), "data/country.json")
with open(COUNTRIES_FILE, encoding="utf-8") as f:
    countries = json.load(f)

COUNTRY_CHOICES = [(country["code"], country["name"]) for country in countries]


class FishingTrip(models.Model):
    country_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default="UA")
    date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def country_name(self) -> str:
        return dict(COUNTRY_CHOICES).get(self.country_code, self.country_code)

    def __str__(self):
        return f"Fishing trip to {self.country_name()} ({self.date})"

    @property
    def total_weight(self) -> Decimal:
        return self.catches.aggregate(
            total=Sum(F("weight") * F("amount"), output_field=DecimalField())
        )["total"] or Decimal("0")

    @property
    def total_fish_amount(self) -> int:
        return self.catches.aggregate(total=Sum("amount"))["total"] or 0


class FishType(models.Model):
    name = models.CharField(max_length=45, unique=True, blank=False)

    class Meta:
        verbose_name = "Fish type"
        verbose_name_plural = "Fish types"

    def __str__(self):
        return self.name


class Catch(models.Model):
    fishing_trip = models.ForeignKey(
        FishingTrip, on_delete=models.CASCADE, related_name="catches"
    )
    fish_type = models.ForeignKey(
        FishType, on_delete=models.CASCADE, related_name="catches"
    )
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    amount = models.PositiveSmallIntegerField(default=0, help_text="Quantity of fish")
    photo = models.ImageField(upload_to="catches/", blank=True, null=True)

    def __str__(self):
        if self.weight:
            return f"{self.amount} × {self.fish_type} ({self.weight} kg each)"
        return f"{self.amount} × {self.fish_type}"

    @property
    def total_weight(self):
        return (self.weight or Decimal("0")) * (self.amount or 0)
