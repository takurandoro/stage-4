from django.db import models

# Create your models here.
class Resident(models.Model):

    name = models.CharField(max_length=100, unique=True)
    size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = "Single", "Single"
        DOUBLE = "Double", "Double"
        SMOOKING = "Smooking", "Smooking"
        NON_SMOOKING = "Non-smooking", "Non-smooking"

    name = models.CharField(max_length=100, unique=True)
    room_type = models.CharField(max_length=50, choices=RoomType.choices)
    floor = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resident = models.ForeignKey(
        Resident, on_delete=models.CASCADE, related_name="rooms"
    )

    def __str__(self):
        return self.name
