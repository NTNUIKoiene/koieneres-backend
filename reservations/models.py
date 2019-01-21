# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Cabin(models.Model):
    name = models.TextField()
    size = models.IntegerField()
    member_price = models.FloatField()
    non_member_price = models.FloatField()

    def __str__(self):
        return self.name


class ReservationMetaData(models.Model):
    membership_number = models.TextField()
    name = models.TextField()
    phone = models.TextField()
    email = models.EmailField()
    should_pay = models.BooleanField()
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        related_name='reservations',
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return str(self.created_at) + " - " + self.email


class Reservation(models.Model):
    cabin = models.ForeignKey(
        Cabin, on_delete=models.CASCADE, related_name='reservation_items')
    date = models.DateField()
    members = models.IntegerField()
    non_members = models.IntegerField()
    meta_data = models.ForeignKey(
        ReservationMetaData,
        on_delete=models.CASCADE,
        related_name='reservation_items')
