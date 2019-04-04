# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_cabin_board = models.BooleanField(default=False)
