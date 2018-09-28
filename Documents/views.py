from rest_framework import viewsets
from Documents.models import AppUser, Project
from Documents.serializers import AppUserSerializers, ProjectSerializers
from django.contrib.auth.models import User
from Documents.serializers import UserSerializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils import timezone
from Documents.permissions import AppUserAdminPermissions
from rest_framework import status
# Create your views here.

class AppUserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (AppUserAdminPermissions,)

    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializers

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (AppUserAdminPermissions,)

    queryset = User.objects.all()
    serializer_class = UserSerializers

class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AppUserAdminPermissions,)

    queryset = Project.objects.all()
    serializer_class = ProjectSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LoginViewSet(ObtainAuthToken):
    #authentication_classes = (BasicAuthentication,)
    #permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            createdTime = token.created
            now = timezone.now()
            interval = now - createdTime
            intervalHours = interval.total_seconds()/60/60
            print (intervalHours)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })