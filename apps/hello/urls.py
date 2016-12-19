
from django.conf.urls import patterns, url
from apps.hello.views import RequestsView, ProfileUpdateView


urlpatterns = patterns(
    'apps.hello.views',
    url(r'^$', 'home', name='home'),
    url(r'^request/$', RequestsView.as_view(), name='request'),
    url(r'^request/edit/(?P<req_id>\d+)/$', 'request_edit',
        name='request_edit'),
    url(r'^edit/(?P<pk>\d+)/$', ProfileUpdateView.as_view(), name='edit'),
    url(r'^userchat/$', 'userchat', name='user_chat'),
    url(r'^send/$', 'send', name='send_chat'),
    url(r'^south/$', 'fix_migrations_on_barista', name='south'),
)
