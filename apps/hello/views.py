from django.shortcuts import render
from .models import AboutMe
import json
from django.http import HttpResponse


def home(request):
    bio = AboutMe.objects.first()

    return render(request, 'home.html', {'bio': bio})


def hard_coded_requests(request):
    tentop = ()
    for i in range(10):
        tentop += (
                  {'method': 'GET',
                   'path': '/request/',
                   'status_code': '200',
                   'date': 'October 19, 2016, 09:30 a.m.'},
                  )

    if request.is_ajax():
        data = json.dumps(tentop)
        return HttpResponse(data, content_type='application/json')

    return render(request,
                  'request.html',
                  {'object_list': tentop})
