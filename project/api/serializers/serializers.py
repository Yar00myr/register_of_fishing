from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import FishingTrip, Catch


class CatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catch
        fields = "__all__"

    def validate(self, data):
        weight = data.get("weight")
        amount = data.get("amount", 0)

        if amount > 0 and not weight:
            raise serializers.ValidationError("Weight must be provided if amount > 0")

        return data

    def validate_weight(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        return round(value, 2) if value is not None else value

    def validate_fish_type(self, value):
        if value is None:
            raise serializers.ValidationError("Fish type must be selected")
        return value

    def validate_photo(self, value):
        if not value:
            return value

        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Photo size must not exceed 10 MB")

        valid_formats = ["image/jpeg", "image/png", "image/webp"]
        if hasattr(value, "content_type") and value.content_type not in valid_formats:
            raise serializers.ValidationError(
                "Only JPEG, PNG, and WEBP formats are allowed"
            )

        return value


class FishingTripSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()
    catches = CatchSerializer(many=True, required=False)

    class Meta:
        model = FishingTrip
        fields = ["id", "country_code", "country_name", "date", "catches"]

    def create(self, validated_data):
        catches_data = validated_data.pop("catches", [])
        fishing_trip = FishingTrip.objects.create(**validated_data)
        for catch_data in catches_data:
            Catch.objects.create(fishing_trip=fishing_trip, **catch_data)
        return fishing_trip

    def update(self, instance, validated_data):
        catches_data = validated_data.pop("catches", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if catches_data is not None:
            instance.catches.all().delete()
            for catch_data in catches_data:
                Catch.objects.create(fishing_trip=instance, **catch_data)
        return instance

    def get_country_name(self, obj):
        return obj.country_name()

    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):

        password = attrs.get("password")

        if not password:
            raise serializers.ValidationError("Password is required.")

        user_obj = User.objects.first()
        if not user_obj:
            raise serializers.ValidationError("No user exists in the database.")

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid password.")

        attrs["user"] = user
        return attrs
