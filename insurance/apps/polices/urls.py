from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns


urlpatterns = patterns('polices.views',
                       url(r'^$', "create_call_request", name='call'),
                       )
