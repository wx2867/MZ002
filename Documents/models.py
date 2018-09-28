from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone

# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, unique= True, on_delete=models.CASCADE)
    typeChoices = (
        ('Admin', 'Admin'),
        ('SuperUser', 'SuperAdmin'),
        ('User', 'User'),
        ('Visitor', 'Visitor'),
    )
    accountType = models.CharField(choices= typeChoices, max_length=20, default='Visitor')

class Project(models.Model):
    projectNumber = models.CharField(max_length=20, null=False, blank=False,unique=True, editable=False)
    description = models.CharField(max_length=255,default='')
    manager = models.ForeignKey(AppUser, related_name='Manager', blank=True, null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(AppUser, related_name='Creator', blank=True, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(AppUser, blank=True, null=True)
    createDate = models.DateTimeField(default=timezone.now())
    modDate = models.DateTimeField(auto_now=True)

class Documents(models.Model):
    creator = models.ForeignKey(related_name='Creator', AppUser, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(related_name='Project', Project, blank=True, null=True, on_delete=models.SET_NULL)
    docNum = models.IntegerField(unique=True, editable=False)
    children = models.ManyToManyField('Documents', blank=True, null=True, on_delete=models.SET_NULL)
    attachment = models.ManyToManyField('Documents', blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=20, default='unknown')
    createDate = models.DateTimeField(default=timezone.now())
    #file = models.FilePathField()
