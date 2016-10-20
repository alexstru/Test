from django.shortcuts import render
from .models import AboutMe, RequestContent
from django.views.generic import ListView
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import os.path
from urlparse import urlparse


def home(request):
    bio = None
    photo_exists = False

    # check if there are entries in the db
    try:
        bio = AboutMe.objects.first()

    except IndexError:
        pass

    if bio:
        # check if user clear image in edit.html
        try:
            host = os.path.abspath(__file__)

            for i in range(4):
                host = os.path.dirname(host)

            name = urlparse(bio.photo.url).path

        except ValueError:
            return render(request,
                          'home.html',
                          {'bio': bio, 'photo_exists': photo_exists})

        # check if user deletes image in file system
        try:
            if os.path.isfile(host + name):
                photo_exists = True
        except IOError:
            pass

    return render(request,
                  'home.html',
                  {'bio': bio, 'photo_exists': photo_exists})


class RequestsView(ListView):
    model = RequestContent
    queryset = RequestContent.objects.order_by('-date')[:10]
    template_name = 'request.html'

    def get(self, request, **kwargs):
        if request.is_ajax():

            jsonDict = {
                "dbcount": len(RequestContent.objects.all()),
                "reqlogs": list(self.get_queryset().values())
            }

            return HttpResponse(json.dumps(jsonDict, default=lambda x: str(x)),
                                content_type="application/json")

        return super(RequestsView, self).get(request, **kwargs)


@csrf_exempt
def edit(request):
    return render(request, 'edit.html')
