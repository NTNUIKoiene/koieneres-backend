# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Reservation(models.Model):
    membership_number = models.TextField()
    name = models.TextField()
    phone = models.TextField()
    email = models.EmailField()
    should_pay = models.BooleanField()
    is_payed = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        'auth.User',
        related_name='reservations',
        on_delete=models.SET_NULL,
        null=True)
