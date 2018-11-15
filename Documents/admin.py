from django.contrib import admin
from Documents import models
# Register your models here.
admin.site.register([models.Documents, models.AppUser, models.Project])