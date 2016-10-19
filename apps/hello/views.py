from django.shortcuts import render
from .models import AboutMe


def home(request):
    bio = AboutMe.objects.first()

    return render(request, 'home.html', {'bio': bio})


def hard_coded_requests(request):
    return render(request, 'request.html', {'num': range(10)})
