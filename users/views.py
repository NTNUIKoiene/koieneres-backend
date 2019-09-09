from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

from users.serializers import UserSerializer

# Create your views here.


class CurrentUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Get the current logged in user
    """

    permission_classes = (permissions.AllowAny,)

    def list(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
