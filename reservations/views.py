# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.dateutils import compute_reservation_period, string_to_date
from utils.pdf import generate_pdf

from .models import (Cabin, CabinClosing, ExtendedPeriod, Reservation,
                     ReservationMetaData)
from .serializers import (CabinClosingListSerializer, CabinClosingSerializer,
                          CabinSerializer, ExtendedPeriodSerializer,
                          PublicReservationMetaDataSerializer,
                          ReservationMetaDataSerializer, StatusSerializer)


class ReservationDataFilter(filters.FilterSet):
    after_date = filters.DateFilter(
        field_name='reservation_items__date', lookup_expr='gte', distinct=True)

    class Meta:
        model = ReservationMetaData
        fields = ('is_paid', 'should_pay', 'id')


class ReservationDataViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = ReservationMetaDataSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filterset_class = ReservationDataFilter
    http_method_names = ['get', 'head', 'patch']

    def get_queryset(self):
        return ReservationMetaData.objects.all()

    @action(detail=True, methods=['GET'])
    def receipt(self, request, pk=None):
        try:
            reservation_metadata = ReservationMetaData.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404
        reservation_items = Reservation.objects.filter(
            meta_data=reservation_metadata)
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = f"inline; filename=kvittering_{reservation_metadata.id}.pdf"
        generate_pdf(response, reservation_metadata, reservation_items)
        return response


class PublicReservationDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReservationMetaData.objects.filter(
        reservation_items__date__gte=datetime.date.today())
    serializer_class = PublicReservationMetaDataSerializer
    permission_classes = (permissions.AllowAny, )

    # TODO: Change which fields are shown on public receipt
    @action(detail=True, methods=['GET'])
    def receipt(self, request, pk=None):
        try:
            reservation_metadata = ReservationMetaData.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404
        reservation_items = Reservation.objects.filter(
            meta_data=reservation_metadata)
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = f"inline; filename=kvittering_{reservation_metadata.id}.pdf"
        generate_pdf(response, reservation_metadata, reservation_items)
        return response


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


class CabinClosingViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'delete']

    def get_queryset(self):
        return CabinClosing.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CabinClosingListSerializer
        return CabinClosingSerializer


class CabinViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CabinSerializer
    queryset = Cabin.objects.all()


class ExtendedPeriodViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'delete']
    queryset = ExtendedPeriod.objects.all()
    serializer_class = ExtendedPeriodSerializer
