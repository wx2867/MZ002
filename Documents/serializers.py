from rest_framework import serializers
from Documents.models import AppUser, Project, Documents
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status


class AppUserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    #password = serializers.CharField(source='user.password')
    #accountType = serializers.CharField()

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'accountType', 'url')

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
    manager=serializers.HyperlinkedRelatedField (view_name='appuser-detail', allow_null=True, queryset=AppUser.objects, required=False)
    creator=serializers.HyperlinkedRelatedField (view_name='appuser-detail', allow_null=True, read_only=True)
    members=serializers.HyperlinkedRelatedField (view_name='appuser-detail', many=True, queryset=AppUser.objects, required=False)
    #projectNumber = serializers.ReadOnlyField()
    createDate = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ('createDate', 'projectNumber', 'manager', 'members', 'url', 'creator', 'description')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', '')
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        localUser = User.objects.get(username=self.user)
        validated_data['creator'] = (AppUser.objects.get(user=localUser))
        return super().create(validated_data,)

    def update(self, instance, validated_data):
        validated_data.pop('projectNumber','')
        return super().update(instance, validated_data)


class DocumentStateSerializers(serializers.ModelSerializer):
    stateChoice = (
        (10, 'In work'), (20, 'Lock'), (30, 'Design state'), (40, 'Release'),
    )
    state = serializers.ChoiceField(choices=stateChoice, required=False)
    docNum = serializers.ReadOnlyField()

    class Meta:
        model = Documents
        fields = ('docNum', 'state')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', '')
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        newInstance = super().update(instance, validated_data)
        state = newInstance.state
        if state>10:
            newInstance.user = AppUser.objects.get(user=User.objects.get(username=self.user))
        else:
            newInstance.user = None
        instance.save()
        return newInstance


class DocumentSerializers(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField (view_name='appuser-detail', allow_null=True, read_only=True)
    project = serializers.HyperlinkedRelatedField (view_name='project-detail', allow_null=True, queryset=Project.objects, required=False)
    children = serializers.SlugRelatedField(many=True, slug_field='docNum', queryset=Documents.objects, required=False)
    attachment = serializers.SlugRelatedField(many=True, slug_field='docNum', queryset=Documents.objects, required=False)
    createDate = serializers.ReadOnlyField()
    docNum = serializers.ReadOnlyField()
    file = serializers.FileField(required=False)
    state = serializers.ReadOnlyField()
    user = serializers.HyperlinkedRelatedField(view_name='appuser-detail', allow_null=True, read_only=True)

    typeChoice = (
        ('CATPart', 'CATPart'),
        ('CATProduct', 'CATProduct'),
        ('PNG', 'PNG'),
        ('Unknown', 'Unknown'),
    )
    type = serializers.ChoiceField(choices=typeChoice, required=False)

    class Meta:
        model = Documents
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', '')
        self.upload = kwargs.pop('upload', False)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        localUser = User.objects.get(username=self.user)
        validated_data['creator'] = (AppUser.objects.get(user=localUser))
        latestDoc = Documents.objects.last()
        if latestDoc:
            latestNum = latestDoc.docNum + 1
        else:
            latestNum = 1
        validated_data['docNum'] = latestNum
        return super().create(validated_data,)

    def update(self, instance, validated_data):
        state = instance.state
        if state>10 and (not self.upload):
            raise serializers.ValidationError('The file is n润ot allowed to modify, please check the status')
        return super().update(instance, validated_data)
