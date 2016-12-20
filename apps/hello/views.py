# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from .models import AboutMe, RequestContent, Thread, Message
from django.views.generic import ListView, UpdateView
from .forms import ProfileUpdateForm, RequestUpdateForm, MessageForm
from django.http import HttpResponse, HttpResponseBadRequest, Http404
import json
import utils
from django.core.urlresolvers import reverse
import logging
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.auth.models import User
from django.conf import settings
import time


logger = logging.getLogger(__name__)
SLEEP_SECONDS = 20


def home(request):
    bio = None
    photo_exists = False

    # check if there are entries in the db
    try:
        bio = AboutMe.objects.first()

    except IndexError:
        pass

    if bio:
        host, name = utils.check_no_image_in_db(bio)
        file_path = host + name

        if file_path:
            photo_exists = utils.check_no_image_in_filesystem(file_path)

    return render(request,
                  'home.html',
                  {'bio': bio, 'photo_exists': photo_exists})


@csrf_exempt
def fix_migrations_on_barista(request):
    ''' Solve problem with migrations on barista '''

    command = request.GET.get('act', '')

    if command == 'read_txt':

        fileContent = ''
        text_file = os.path.join(settings.BASE_DIR, 'setup.txt')
        file = open(text_file)

        for line in file:
            fileContent += line

        json_data = {'fileContent': fileContent}
        return HttpResponse(json.dumps(json_data),
                            content_type="application/json")

    result, linebreaks = utils.FixBarista(command)

    return render(request,
                  'south.html',
                  {'result': result,
                   'linebreaks': linebreaks})


class RequestsView(ListView):
    model = RequestContent
    template_name = 'request.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequestsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if 'priority' in self.request.GET:
            priority = self.request.GET.get('priority', '')

            if priority == '1':
                queryset = RequestContent.objects.order_by('-priority')[:10]
            else:
                queryset = RequestContent.objects.order_by('priority')[:10]

        elif 'date' in self.request.GET:
            date = self.request.GET.get('date', '')

            if date == '1':
                queryset = RequestContent.objects.order_by('-date')[:10]
            else:
                queryset = RequestContent.objects.order_by('date')[:10]

        else:
            queryset = RequestContent.objects.order_by('-date')[:10]

        return queryset

    def get(self, request, **kwargs):
        if request.is_ajax():

            jsonDict = {
                "dbcount": len(RequestContent.objects.all()),
                "reqlogs": list(self.get_queryset().values())
            }

            return HttpResponse(json.dumps(jsonDict, default=lambda x: str(x)),
                                content_type="application/json")

        return super(RequestsView, self).get(request, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST

        ''' get RequestContent object for given request '''
        request_content = RequestContent.objects.get(pk=data['pk'])
        request_content.priority = data['priority']
        request_content.save()

        ''' return JSON '''
        json_data = {	'link_id': '#priority_' + str(request_content.id),
                      'priority': request_content.priority}

        return HttpResponse(json.dumps(json_data),
                            content_type="application/json")


@login_required
def request_edit(request, req_id):
    """
    Returns page with form to edit request on GET.
    Validates form and redirects to /request/ on POST."""

    req = get_object_or_404(RequestContent, pk=req_id)

    if request.method == 'GET':
        form = RequestUpdateForm(instance=req)
        return render(request, 'request_edit.html',
                      {'form': form, 'req_id': req_id})

    elif request.method == 'POST':
        form = RequestUpdateForm(request.POST, instance=req)

        if form.is_valid():
            form.save()
            if request.is_ajax():
                profile_to_json = {'status': "success"}
                return HttpResponse(json.dumps(profile_to_json),
                                    content_type="application/json")
            else:
                return redirect(reverse('hello:request'))

        if form.is_invalid():
            return render(request,
                          'hello/request_edit.html',
                          {'form': form, 'req_id': req_id})
    raise Http404


class ProfileUpdateView(UpdateView):
    model = AboutMe
    form_class = ProfileUpdateForm
    template_name = 'edit.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('hello:edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)

        photo_exists = os.path.isfile(self.object.photo.path) \
            if self.object.photo else False

        if not photo_exists:
            message = "File doesn't exist: {}".format(self.object.photo.url) \
                if self.object.photo else "User has no photo"
            logger.exception(message)

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
                    errors_dict[error] = form.errors[error]
            return HttpResponseBadRequest(json.dumps(errors_dict))

        return super(ProfileUpdateView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                return super(ProfileUpdateView,
                             self).post(request, *args, **kwargs)
            except IOError:
                message = "File doesn't exist:  " + self.object.photo.url
                logger.exception(message)
                return HttpResponseBadRequest(
                          json.dumps({'Image': message}),
                          content_type="application/json")

        return super(ProfileUpdateView, self).post(request, *args, **kwargs)


@login_required
def userchat(request):
    threads = Thread.objects.filter(
        participants=request.user
    ).order_by("-lastid")

    if not threads:
        return render(request,
                      'dialogs.html',
                      {'users': User.objects.exclude(username=request.user)})

    for thread in threads:
        partner = thread.participants.exclude(id=request.user.id)
        thread.partner = partner[0].username

    return render(request,
                  'dialogs.html',
                  {
                    'threads': threads,
                    'users': User.objects.exclude(username=request.user)
                  })


@csrf_exempt
@require_POST
def send(request):
    """
    This view is called when the client wants to send a message.
    If the message is saved successfully, 
    200 OK with a body containing 'OK' is returned.
    If it fails, json is returned with a body describing the fault.
    """
    # Parse and validate text.
    form = MessageForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps(form.errors),
                                      content_type="application/json")

    sender_id = int(request.POST['sender_id'])
    mode = request.POST['mode']

    # Define dialog members
    sender = User.objects.get(id=sender_id)
    recipient = User.objects.get(username=request.POST['recipient'])

    # Get the thread corresponding to the dialog members
    thread_queryset = Thread.objects.filter(participants=recipient).\
                                     filter(participants=sender)
    new_thread = ''
    if thread_queryset.exists():
        thread = thread_queryset[0]
    else:
        thread = Thread.objects.create()
        thread.participants.add(sender, recipient)
        new_thread = 'new'

    # Make the new message, and save it in the backend.
    msg = Message()
    msg.sender_id = sender_id
    msg.thread_id = thread.id
    msg.text = form.cleaned_data['text']
    msg.save()

    # Remember last message ID in the thread
    thread.lastid = msg.id
    thread.save()
    
    # If user don`t change dialog and just sends a message to the current one
    if mode == 'currentDialog':
        return HttpResponse('OK', content_type='text/plain; charset=UTF-8')

    # update QuerySet of threads with current user
    threads = Thread.objects.\
                     filter(participants=sender).\
                     order_by("-lastid")

    # prepare data to switch to another dialog
    result = utils._change_current_thread(threads, sender_id, new_thread)

    return HttpResponse(json.dumps(result),
                            content_type="application/json")


@csrf_exempt
@require_POST
def get_new(request):
    """
    This method is called from the client when it wants to check if there are
    any new messages since the last message "id".

    The backend is checked every second for SLEEP_SECONDS. If there are no new
    messages in this interval, "OK" is returned and the client may initiate a
    new request.

    The result of this method, when new messages are available is json similar
    to below:

    {
        messages: [{...}, {...}, ...],
        lastid: 100
    }

    "message" contains HTML that can be injected into a textarea.
     "lastid" is the highest(latest) message ID in the thread.
    """

    thread_id = int(request.POST['thread_id'])
    last_id = int(request.POST['last_id'])
    username = request.POST['username']
    receiver = request.POST['receiver']

    for _ in range(SLEEP_SECONDS):
        # Get the thread corresponding to the dialog members
        thread = Thread.objects.get(id=thread_id)

        # If no messages was found, sleep and try again.
        if thread.lastid == last_id:
            time.sleep(1)
            continue

        # Query the backend for messages since "id".
        messages = Message.objects.\
                           filter(thread=thread_id, pk__gt=last_id).\
                           order_by('pk')

        message_count = messages.count()

        # Never return more than 100 messages at once.
        if message_count > 100:
            messages = messages[message_count - 100:]

        # Convert the QuerySet to a dictlist.
        result = utils._prepear_new_messages(messages)
        return HttpResponse(json.dumps(result),
                            content_type="application/json")

    # If there are no new messages in the interval, "OK" is returned
    return HttpResponse('OK', content_type='text/plain')
