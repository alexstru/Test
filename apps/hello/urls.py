
from django.conf.urls import patterns, url
from apps.hello.views import RequestsView


urlpatterns = patterns(
    'apps.hello.views',
    url(r'^$', 'home', name='home'),
    url(r'^request/$', RequestsView.as_view(), name='request'),
    url(r'^edit/$', 'edit', name='edit'),
)
