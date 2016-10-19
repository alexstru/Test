
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.hello.views',
    url(r'^$', 'home', name='home'),
    url(r'^request/$', 'hard_coded_requests', name='request'),
)
