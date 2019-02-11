# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Reservation, ReservationMetaData, Cabin
from .serializers import ReservationMetaDataSerializer, PublicReservationMetaDataSerializer, StatusSerializer
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from utils.dateutils import compute_reservation_period, string_to_date
import datetime


class ReservationDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReservationMetaData.objects.all()
    serializer_class = ReservationMetaDataSerializer
    permission_classes = (permissions.IsAuthenticated, )


class PublicReservationDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReservationMetaData.objects.filter(
        reservation_items__date__gte=datetime.date.today())
    serializer_class = PublicReservationMetaDataSerializer
    permission_classes = (permissions.AllowAny, )


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    list:
    Get the status for each cabin. Includes how many places are occupied 
    and if the cabin is closed.
    query parameters:
        from: date (default today)
        to: date (default end of current reservation period)


    retrieve:
    Get the status for a single cabin. Includes how many places are occupied 
    and if the cabin is closed.
    query parameters:
        from: date (default today)
        to: date (default end of current reservation period)
    '''
    queryset = Cabin.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = StatusSerializer

    def get_serializer_class(self):
        # TODO: Custom for details?
        return self.serializer_class

    def get_serializer_context(self):
        from_date = self.request.GET.get('from', str(datetime.date.today()))
        to_date = self.request.GET.get('to',
                                       str(compute_reservation_period()['to']))
        return {
            'from': string_to_date(from_date),
            'to': string_to_date(to_date)
        }

    def paginate_queryset(self, queryset, view=None):
        return None


class CreateReservationViewSet(mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = ReservationMetaDataSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ReservationPeriodViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    list:
    Get the current reservation period
    
    retrieve:
    Get the reservation period of a specified date.
    Date format example: 2019-01-20
    '''
    permission_classes = (permissions.AllowAny, )

    def list(self, request, format=None):
        return Response(compute_reservation_period())

    def retrieve(self, request, pk=None):
        return Response(compute_reservation_period(string_to_date(pk)))
