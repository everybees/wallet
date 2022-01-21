from django.urls import path, include
from accounts.views import hello_world, hello_jerry
from rest_framework import routers
from rest_framework.authtoken import views

from .views import UserViewSet, WalletViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register('users', UserViewSet, 'users')
router.register('wallets', WalletViewSet, 'wallets')


urlpatterns = [
    path("", include(router.urls)),
    path("jerry", hello_jerry),
    path('token-auth', views.obtain_auth_token, name='api-auth-token'),

]