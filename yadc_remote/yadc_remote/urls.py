from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_PATH,
        'show_indexes': settings.DEBUG,
    }),
    url(r'^game/', include('web_interface.urls')),
    url(r'^$', 'web_interface.views.root_redirect'),
)
