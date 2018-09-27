from rest_framework import serializers
from Documents.models import AppUser
from django.contrib.auth.models import User

class AppUserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password')
    accountType = serializers.CharField()

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password', 'accountType')

    def create(self, validated_data):
        userData = validated_data.pop('user')

        user, created = User.objects.get_or_create(username=userData['username'], email=userData['email'], password=userData['password'])
        instance = AppUser.objects.create(user=user,**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.accountType = validated_data.get('ban_status', instance.ban_status)
        instance.user.password = validated_data.get('user.password', instance.user.password)
        return instance

class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ('username', 'id')