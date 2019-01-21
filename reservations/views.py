# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Reservation, ReservationMetaData
from .serializers import ReservationMetaDataSerializer, PublicReservationMetaDataSerializer
from rest_framework import viewsets, permissions


class ReservationDataViewSet(viewsets.ModelViewSet):
    queryset = ReservationMetaData.objects.all()
    serializer_class = ReservationMetaDataSerializer
    permission_classes = (permissions.IsAuthenticated, )


class PublicReservationDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReservationMetaData.objects.all()
    serializer_class = PublicReservationMetaDataSerializer