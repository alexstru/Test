from django.shortcuts import render
from .models import AboutMe, RequestContent
from django.views.generic import ListView
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


def home(request):
    bio = AboutMe.objects.first()

    return render(request, 'home.html', {'bio': bio})


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
