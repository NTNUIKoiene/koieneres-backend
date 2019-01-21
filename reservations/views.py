# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Reservation, ReservationMetaData
from .serializers import ReservationSerializer, ReservationMetaDataSerializer
from rest_framework import viewsets, permissions

# Create your views here.


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReservationDataViewSet(viewsets.ModelViewSet):
    queryset = ReservationMetaData.objects.all()
    serializer_class = ReservationMetaDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )