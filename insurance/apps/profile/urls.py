from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from profile.views import profile
from profile.views import edit_persona
from profile.views import delete_persona
from profile.views import policy_list
from profile.views import faq


urlpatterns = patterns('',
                       url(r'^$', profile, name='userprofile_edit'),
                       url(r'^(?P<action>\w+)/$', profile, name='userprofile_edit'),
                       url(r'^add_persona/$', edit_persona, name='userprofile_addpersona'),
                       url(r'^edit_persona/(?P<persona_id>\d+)/$', edit_persona, name='userprofile_editpersona'),
                       url(r'^delete_persona/(?P<persona_id>\d+)/$', delete_persona, name='userprofile_deletepersona'),
                       url(r'^policies/$', policy_list, name='userprofile_policylist'),
                       url(r'^policies/(?P<policy_type>\d+)/$', policy_list, name='userprofile_policylist_type'),
                       url(r'^faq/', faq, name='userprofile_faq')
                       )
