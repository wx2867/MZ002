from rest_framework import permissions
from Documents.models import AppUser
class AppUserAdminPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        theAppUser = AppUser.objects.get(user=user)
        if not theAppUser:
            return False
        print(theAppUser.accountType)
        return theAppUser.accountType == 'Admin'
