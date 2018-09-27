from django.shortcuts import render
from rest_framework import viewsets
from Documents.models import AppUser
from Documents.serializers import AppUserSerializers
from django.contrib.auth.models import User
from Documents.serializers import UserSerializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class AppUserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializers

class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializers

class LoginViewSet(viewsets.ViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        token = Token.objects.create(user=request.user)
        return Response(token.key)

