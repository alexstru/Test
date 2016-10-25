
from django.conf.urls import patterns, url
from apps.hello.views import RequestsView, ProfileUpdateView


urlpatterns = patterns(
    'apps.hello.views',
    url(r'^$', 'home', name='home'),
    url(r'^request/$', RequestsView.as_view(), name='request'),
    url(r'^edit/(?P<pk>\d+)/$', ProfileUpdateView.as_view(), name='edit'),
)
