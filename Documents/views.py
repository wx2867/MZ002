from rest_framework import viewsets
from Documents.models import AppUser, Project, Documents
from Documents.serializers import AppUserSerializers, ProjectSerializers, DocumentSerializers, DocumentStateSerializers
from django.contrib.auth.models import User
from Documents.serializers import UserSerializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils import timezone
from Documents.permissions import AppUserAdminPermissions
from rest_framework import status,mixins
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import action, parser_classes
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend

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


class DocumentsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AppUserAdminPermissions,)
    queryset = Documents.objects.all()
    serializer_class = DocumentSerializers
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('docNum', 'project', 'state', 'type', )

    @action(methods=['get'], detail=True, url_path='File')
    @parser_classes((MultiPartParser ,FileUploadParser))
    def download(self, request, pk=None):
        instance = self.get_object()
        # get an open file handle (I'm just using a file attached to the model for this example):
        file_handle = instance.file.open()
        # send file
        response = FileResponse(file_handle)
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.file.name
        response['Filename'] = instance.file.name

        return response

    @action(methods=['put'], detail=True, url_path='UFile')
    def upload(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DocumentStateSerializers(instance, data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        instanceUser = instance.user
        user = request.user

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, upload=(instanceUser.user==user))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path='State')
    def changeState(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DocumentStateSerializers(instance, data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        instanceUser = instance.user
        user = request.user
        print(user, instanceUser)
        if instanceUser == None:
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if instanceUser.user == user:
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('You are not this doc user')

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