# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.mail import send_reservation_receipt


class Cabin(models.Model):
    article_number = models.IntegerField()
    name = models.TextField()
    size = models.IntegerField()
    member_price = models.FloatField(default=40)
    non_member_price = models.FloatField(default=80)
    in_use = models.BooleanField(default=True)

    def __str__(self):
        return self.name + f" ({self.id})"


class CabinClosing(models.Model):
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    comment = models.TextField(default="")
    avalanche_warning = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="closings",
        on_delete=models.SET_NULL,
        null=True,
    )


class ReservationMetaData(models.Model):
    membership_number = models.TextField()
    name = models.TextField()
    phone = models.TextField()
    email = models.EmailField()
    should_pay = models.BooleanField()
    is_paid = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reservations",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.created_at) + " - " + self.email + f" (#{self.id})"


class Reservation(models.Model):
    cabin = models.ForeignKey(
        Cabin, on_delete=models.CASCADE, related_name="reservation_items", db_index=True
    )
    date = models.DateField(db_index=True)
    members = models.IntegerField()
    non_members = models.IntegerField()
    meta_data = models.ForeignKey(
        ReservationMetaData,
        on_delete=models.CASCADE,
        related_name="reservation_items",
        db_index=True,
    )


class ExtendedPeriod(models.Model):
    # Wednesday where reservation starts
    reservation_date = models.DateField(db_index=True)
    # Thursday where it ends
    end_date = models.DateField(db_index=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.description}, {self.reservation_date} -> {self.end_date}"


@receiver(post_save, sender=ReservationMetaData)
def send_confirmation_mail(sender, instance, created, **kwargs):
    if created:
        recipient = instance.email
        res_id = instance.id
        send_reservation_receipt(res_id, recipient)
