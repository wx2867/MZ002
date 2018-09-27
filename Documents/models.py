from django.db import models
from django.contrib.auth.models import User

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

