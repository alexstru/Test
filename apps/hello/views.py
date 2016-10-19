from django.shortcuts import render
from .models import AboutMe


def home(request):
    bio = AboutMe.objects.first()

    return render(request, 'home.html', {'bio': bio})
