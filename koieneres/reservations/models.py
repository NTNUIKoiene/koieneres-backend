# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Reservation(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    name = models.TextField()
    created_by = models.ForeignKey(
        'auth.User',
        related_name='reservations',
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        ordering = ('from_date', 'to_date')
