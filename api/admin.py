from django.contrib import admin
from .models import *


# Register your models here.


class ResidentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "size",
        "created_at",
        "updated_at",
    )


admin.site.register(Resident, ResidentAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "floor",
        "room_type",
        "resident",
        "created_at",
        "updated_at",
    )


admin.site.register(Room, RoomAdmin)
