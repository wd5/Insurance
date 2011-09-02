from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns


urlpatterns = patterns('profile.views',
                       url(r'^$', "profile", name='userprofile_edit'),
#                       url(r'^(?P<action>\w+)/$', "profile", name='userprofile_edit'),
                       url(r'^add_persona/$', "add_persona", name='userprofile_addpersona'),
                       url(r'^edit_persona/(?P<persona_id>\d+)/$', "edit_persona", name='userprofile_editpersona'),
                       url(r'^delete_persona/(?P<persona_id>\d+)/$', "delete_persona", name='userprofile_deletepersona'),
                       url(r'^policies/$', "policy_list", name='userprofile_policylist'),
                       url(r'^policies/(?P<policy_type>\d+)/$', "policy_list", name='userprofile_policylist_type'),
                       url(r'^faq/', "faq", name='userprofile_faq')
                       )
