from django.urls import path, include
from accounts.views import hello_world, hello_jerry
from rest_framework import routers

from .views import UserViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register('users', UserViewSet, 'users')

urlpatterns = [
    path("", include(router.urls)),
    path("jerry", hello_jerry),

]