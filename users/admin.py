from django.contrib import admin
from django.contrib.auth.models import Group

from main.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")


admin.site.unregister(Group)
