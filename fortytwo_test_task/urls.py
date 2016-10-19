from django.conf.urls import patterns, include, url
from django.contrib import admin
from fortytwo_test_task.settings.common import MEDIA_ROOT, DEBUG
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.hello import urls as hello_urls


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include(hello_urls, namespace='hello')),
    url(r'^admin/', include(admin.site.urls)),
) + staticfiles_urlpatterns()

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns(
        '',
        (r'^uploads/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': MEDIA_ROOT}),
        )
