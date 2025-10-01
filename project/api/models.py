import json
import os
from django.db import models

COUNTRIES_FILE = os.path.join(os.path.dirname(__file__), "data/country.json")
with open(COUNTRIES_FILE, encoding="utf-8") as f:
    countries = json.load(f)

COUNTRY_CHOICES = [(c["code"], c["name"]) for c in countries]


class FishingTrip(models.Model):
    country_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default="UA")
    date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def country_name(self) -> str:
        return dict(COUNTRY_CHOICES).get(self.country_code, self.country_code)

    def __str__(self):
        return f"Fishing trip to {self.country_name()} ({self.date})"

    @property
    def total_weight(self) -> float:
        return sum((catch.total_weight or 0) for catch in self.catches.all())

    @property
    def total_fish_amount(self) -> int:
        return sum(catch.amount for catch in self.catches.all())


class Catch(models.Model):
    fishing_trip = models.ForeignKey(
        FishingTrip, on_delete=models.CASCADE, related_name="catches"
    )
    fish_type = models.CharField(max_length=45)
    weight = models.FloatField(blank=True, null=True)
    amount = models.PositiveSmallIntegerField(default=0, help_text="Quantity of fish")
    photo = models.ImageField(upload_to="catches/", blank=True, null=True)

    def __str__(self):
        return f"{self.fish_type} ({self.weight or '—'} kg)"

    @property
    def total_weight(self):
        return (self.weight or 0) * (self.amount or 0)
