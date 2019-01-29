# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Reservation, ReservationMetaData, Cabin
from .serializers import ReservationMetaDataSerializer, PublicReservationMetaDataSerializer, CabinStatusSerializer
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from utils.dateutils import compute_reservation_period
import datetime


class ReservationDataViewSet(viewsets.ModelViewSet):
    queryset = ReservationMetaData.objects.all()
    serializer_class = ReservationMetaDataSerializer
    permission_classes = (permissions.IsAuthenticated, )


class PublicReservationDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReservationMetaData.objects.all()
    serializer_class = PublicReservationMetaDataSerializer


class CabinStatusViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Return a list of the status for cabins for each date. The status includes 
    how many of the places that are booked and if the cabin is closed. Also
    returns the name, size and price of the cabin.
    '''
    queryset = Cabin.objects.all()
    serializer_class = CabinStatusSerializer

    def get_serializer_class(self):
        # TODO: Custom for details?
        return self.serializer_class

    def get_serializer_context(self):
        from_date = self.request.GET.get('from', datetime.date.today())
        to_date = self.request.GET.get(
            'to',
            datetime.date.today() + datetime.timedelta(days=14))
        return {'from': from_date, 'to': to_date}


class ReservationPeriodViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    list:
    Get the current reservation period
    
    retrieve:
    Get the reservation period of a specified date
    '''

    def list(self, request, format=None):
        return Response(compute_reservation_period())

    def retrieve(self, request, pk=None):
        return Response(
            compute_reservation_period(
                datetime.datetime.strptime(pk, "%Y-%m-%d").date()))
