# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Reservation, ReservationMetaData, Cabin, ExtendedPeriod

# Register your models here.

admin.site.register(Reservation)
admin.site.register(ReservationMetaData)
admin.site.register(Cabin)
admin.site.register(ExtendedPeriod)