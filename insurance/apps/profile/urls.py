from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from profile.views import profile
from profile.views import policy_list



urlpatterns = patterns('',
                       url(r'^$', profile, name='userprofile_edit'),
                       url(r'^policies/$', policy_list, name='userprofile_policylist'))
