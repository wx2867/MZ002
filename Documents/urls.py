from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from Documents import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.AppUserViewSet)
router.register(r'LocalUsers', views.UserViewSet)
router.register(r'project', views.ProjectViewSet)
#router.register(r'Login', views.LoginViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^Login/',views.LoginViewSet.as_view())
]