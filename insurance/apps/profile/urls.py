from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from profile.views import profile



urlpatterns = patterns('',
                       url(r'^$', profile, name='userprofile_edit'))
