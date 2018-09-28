from rest_framework import serializers
from Documents.models import AppUser, Project, Documents
from django.contrib.auth.models import User

class AppUserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password')
    #accountType = serializers.CharField()

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password', 'accountType', 'url')

    def create(self, validated_data):
        userData = validated_data.pop('user')
        length = len(User.objects.filter(username=userData['username']))
        if length>0:
            #Already exist
            return ('Acount already exist!')
        user = User.objects.create_user(username=userData['username'], email=userData['email'], password=userData['password'])
        instances = AppUser.objects.create(user=user,**validated_data)
        return instances

    def update(self, instance, validated_data):
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.accountType = validated_data.get('accountType', instance.ban_status)
        instance.user.password = validated_data.get('user.password', instance.user.password)
        return instance

class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ('username', 'id', 'password')

class ProjectSerializers(serializers.HyperlinkedModelSerializer):
    manager=serializers.HyperlinkedRelatedField (view_name='appuser-detail', allow_null=True, read_only=True)
    creator=serializers.HyperlinkedRelatedField (view_name='appuser-detail', allow_null=True, read_only=True)
    members=serializers.HyperlinkedRelatedField (view_name='appuser-detail', many=True, allow_null=True, queryset=AppUser)
    #projectNumber = serializers.ReadOnlyField()
    createDate = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ('createDate', 'projectNumber', 'manager', 'members', 'url', 'creator', 'description')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
    def create(self, validated_data):
        localUser = User.objects.get(username=self.user)
        validated_data['creator'] = (AppUser.objects.get(user=localUser))
        return super().create(validated_data,)

class DocumentSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Documents
        fields = '__all__'
