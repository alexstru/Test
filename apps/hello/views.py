from django.shortcuts import render
from .models import AboutMe, RequestContent
from django.views.generic import ListView
from django.core import serializers
from django.http import HttpResponse


def home(request):
    bio = AboutMe.objects.first()

    return render(request, 'home.html', {'bio': bio})


class RequestsView(ListView):
    model = RequestContent
    queryset = RequestContent.objects.order_by('-date')[:10]
    template_name = 'request.html'

    def get(self, request, **kwargs):
        if request.is_ajax():
            self.object_list = self.get_queryset()
            data = serializers.serialize("json", self.get_queryset())
            return HttpResponse(data, content_type='application/json')

        return super(RequestsView, self).get(request, **kwargs)
