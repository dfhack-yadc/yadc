from django.conf.urls import patterns, include, url

urlpatterns = patterns('web_interface.views',
    url(r'^$', 'main')
)
