from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_cabin_board = models.BooleanField(default=False)
