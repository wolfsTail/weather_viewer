from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='E-mail')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
