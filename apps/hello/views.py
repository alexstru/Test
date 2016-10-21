from django.shortcuts import render
from .models import AboutMe, RequestContent
from django.views.generic import ListView, UpdateView
from .forms import ProfileUpdateForm
from django.http import HttpResponse, HttpResponseBadRequest
import json
import os.path
from urlparse import urlparse
from django.core.urlresolvers import reverse


def check_no_image_in_db(model_instance):
    ''' check if user clear image in db '''

    host = ''
    name = ''

    try:
        host = os.path.abspath(__file__)

        for i in range(4):
            host = os.path.dirname(host)

        name = urlparse(model_instance.photo.url).path

    except ValueError:
        pass

    return host, name


def check_no_image_in_filesystem(file_path):
    ''' check if user deletes image in file system '''

    photo_exists = False

    try:
        if os.path.isfile(file_path):
            photo_exists = True
    except IOError:
        pass

    return photo_exists


def home(request):
    bio = None
    photo_exists = False

    # check if there are entries in the db
    try:
        bio = AboutMe.objects.first()

    except IndexError:
        pass

    if bio:
        host, name = check_no_image_in_db(bio)
        file_path = host + name

        if file_path:
            photo_exists = check_no_image_in_filesystem(file_path)

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


class ProfileUpdateView(UpdateView):
    model = AboutMe
    form_class = ProfileUpdateForm
    template_name = 'edit.html'

    def get_success_url(self):
        return reverse('hello:edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        photo_exists = False

        host, name = check_no_image_in_db(self.object)
        file_path = host + name

        if file_path:
            photo_exists = check_no_image_in_filesystem(file_path)

        context['photo_exists'] = photo_exists
        return context

    def form_valid(self, form):
        """
        If the request is ajax, save the form and return a json response.
        Otherwise return super as expected.
        """

        if self.request.is_ajax():
            form.save()
            profile_to_json = {'status': "success"}
            return HttpResponse(json.dumps(profile_to_json),
                                content_type="application/json")

        return super(ProfileUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        If the request is ajax, save the form and return a json response.
        Otherwise return super as expected.
        """

        if self.request.is_ajax():
            errors_dict = {}
            if form.errors:
                for error in form.errors:
                    e = form.errors[error]
                    errors_dict[error] = e
            return HttpResponseBadRequest(json.dumps(errors_dict))

        return super(ProfileUpdateView, self).form_invalid(form)
