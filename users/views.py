from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins
from users.serializers import UserSerializer
from rest_framework.response import Response

# Create your views here.


class CurrentUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
