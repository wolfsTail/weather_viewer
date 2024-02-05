from django.db import models
from traitlets import default

from users.models import User


class Location(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name="Пользователь",
    )
    latitude = models.FloatField(verbose_name="Широта", default=0.0)
    longitude = models.FloatField(verbose_name="Долгота", default=0.0)

    def __str__(self):
        return f"{self.name}: lat:{self.latitude}, lon:{self.longitude}"
