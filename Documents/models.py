from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone

# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, related_name='User', unique= True, on_delete=models.CASCADE)
    typeChoices = (
        ('Admin', 'Admin'),
        ('SuperUser', 'SuperAdmin'),
        ('User', 'User'),
        ('Visitor', 'Visitor'),
    )
    accountType = models.CharField(choices= typeChoices, max_length=20, default='Visitor')
    def __str__(self):
        return self.user.username

class Project(models.Model):
    projectNumber = models.CharField(max_length=20, null=False, blank=False,unique=True)
    description = models.CharField(max_length=255,default='')
    manager = models.ForeignKey(AppUser, related_name='Manager', blank=True, null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(AppUser, related_name='Creator', blank=True, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(AppUser, blank=True)
    createDate = models.DateTimeField(default=timezone.now())
    modDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.projectNumber

def user_directory_path(instance, filename):
    return '{0}_{1}/{2}'.format(instance.docNum, instance.type, filename)

class Documents(models.Model):
    creator = models.ForeignKey(AppUser, related_name='DocCreator', blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, related_name='DocProject', blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(AppUser, related_name='Locker', blank=True, null=True, on_delete=models.SET_NULL)
    docNum = models.IntegerField(unique=True)
    children = models.ManyToManyField('Documents', related_name='DocChildren', blank=True)
    attachment = models.ManyToManyField('Documents', related_name='DocAttachment', blank=True)
    type = models.CharField(max_length=20, default='unknown')
    createDate = models.DateTimeField(default=timezone.now())
    file = models.FileField(upload_to=user_directory_path, null=True)
    state = models.IntegerField(default=0)
    #modDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.docNum)
