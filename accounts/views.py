from django.shortcuts import render

# Create your views here.


def hello_world(request):
    return render(request, "hello_world.html")


def hello_jerry(request):
    return render(request, "hello_jerry.html")
