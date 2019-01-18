# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Reservation(models.Model):
    fromDate = models.DateField()
    toDate = models.DateField()
    name = models.TextField()

    class Meta:
        ordering = ('fromDate', 'toDate')
