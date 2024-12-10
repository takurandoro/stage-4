from rest_framework import serializers
from .models import Room, Resident
from django.contrib.auth.models import User


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ("id", "name", "size")


class RoomSerializer(serializers.ModelSerializer):
    resident = Resident
    resident_name = serializers.ReadOnlyField(source="resident.name")

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "floor",
            "room_type",
            "resident_name",
            "resident",
        )
        extra_kwargs = {
            "resident": {"write_only": True},
        }

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user        