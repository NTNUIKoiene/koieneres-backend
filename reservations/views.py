# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.dateutils import compute_reservation_period, string_to_date
from .models import Cabin, CabinClosing, ExtendedPeriod, ReservationMetaData
from .serializers import (
    CabinClosingListSerializer,
    CabinClosingSerializer,
    CabinSerializer,
    ExtendedPeriodSerializer,
    ReservationMetaDataSerializer,
    StatusSerializer,
)


class ReservationDataFilter(filters.FilterSet):
    after_date = filters.DateFilter(
        field_name="reservation_items__date", lookup_expr="gte", distinct=True
    )

    class Meta:
        model = ReservationMetaData
        fields = ("is_paid", "should_pay", "id")


class ReservationDataViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    list:
    List all cabin reservations

    retrieve:
    Get cabin reservation by id

    partial_update:
    Change an existing reservation

    """

    serializer_class = ReservationMetaDataSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = ReservationDataFilter
    http_method_names = ["get", "head", "patch"]

    def get_queryset(self):
        return ReservationMetaData.objects.all()

    @action(detail=True, methods=["GET"], permission_classes=[permissions.AllowAny])
    def receipt(self, request, pk=None):
        """
        Get receipt data of reservation
        """
        try:
            reservation_metadata = ReservationMetaData.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404
        return Response(
            {
                "metadata": ReservationMetaDataSerializer(reservation_metadata).data,
                "ean": "5901234123457",
            }
        )


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
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
    """

    queryset = Cabin.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = StatusSerializer

    def get_serializer_class(self):
        # TODO: Custom for details?
        return self.serializer_class

    def get_serializer_context(self):
        from_date = self.request.GET.get("from", str(datetime.date.today()))
        to_date = self.request.GET.get(
            "to", str(compute_reservation_period(ExtendedPeriod.objects.all())["to"])
        )
        return {"from": string_to_date(from_date), "to": string_to_date(to_date)}

    def paginate_queryset(self, queryset, view=None):
        return None


class CreateReservationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
    Create a new reservation
    """

    serializer_class = ReservationMetaDataSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ReservationPeriodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Get the current reservation period
    
    retrieve:
    Get the reservation period of a specified date.
    Date format example: 2019-01-20
    """

    permission_classes = (permissions.AllowAny,)

    def list(self, request, format=None):
        return Response(compute_reservation_period(ExtendedPeriod.objects.all()))

    def retrieve(self, request, pk=None):
        return Response(
            compute_reservation_period(ExtendedPeriod.objects.all(), string_to_date(pk))
        )


class CabinClosingViewSet(viewsets.ModelViewSet):
    """
    list:
    Get information about cabin all closings

    create:
    Close a cabin for a period of time

    retrieve:
    Get a single cabin closing

    delete:
    Delete a cabin closing
    """

    http_method_names = ["get", "post", "head", "delete"]

    def get_queryset(self):
        return CabinClosing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CabinClosingListSerializer
        return CabinClosingSerializer


class CabinViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Get list of all cabins
    """

    serializer_class = CabinSerializer
    queryset = Cabin.objects.all()


class ExtendedPeriodViewSet(viewsets.ModelViewSet):
    """
    list:
    Get all extended reservation periods

    retrieve:
    Get extended reservation period by id

    create:
    Create a new reservation period exension

    delete:
    Delete a reservation period extension
    """

    http_method_names = ["get", "post", "head", "delete"]
    queryset = ExtendedPeriod.objects.all()
    serializer_class = ExtendedPeriodSerializer
