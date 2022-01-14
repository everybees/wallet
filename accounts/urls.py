from django.urls import path
from accounts.views import hello_world, hello_jerry


urlpatterns = [
    path("", hello_world),
    path("jerry", hello_jerry)
]