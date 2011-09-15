from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
#from notification.views import notices, mark_all_seen, feed_for_user, single, notice_settings
from ins_notification.views import question,answer,ins_single

urlpatterns = patterns('',
                       #url(r'^$', inbox, name="ins_notification_inbox"),
                       #url(r'^(\d+)/$', ins_single, name="ins_notification_notice"),
                       url(r'^question_success/$', direct_to_template,
                            {'template': 'notification/success.html'},
                            name='question_success'),
                       url(r'^question/$',question, name="ins_notification_question"),
                       url(r'^answer/(\d+)/$', answer,name="ins_notification_answer"),
                       #url(r'^$', notices, name="notification_notices"),
                       #url(r'^settings/$', notice_settings, name="notification_notice_settings"),
                       #url(r'^(\d+)/$', single, name="notification_notice"),
                       #url(r'^feed/$', feed_for_user, name="notification_feed_for_user"),
                       #url(r'^mark_all_seen/$', mark_all_seen, name="notification_mark_all_seen"),
                       )
