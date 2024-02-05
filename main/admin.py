from django.contrib import admin

from main.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
