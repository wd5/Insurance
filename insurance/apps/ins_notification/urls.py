from django.conf.urls.defaults import *

from notification.views import notices, mark_all_seen, feed_for_user, single, notice_settings
from ins_notification.views import inbox,question


urlpatterns = patterns('',
    url(r'^$', inbox, name="ins_notification_inbox"),
    url(r'^question/$', question, name="ins_notification_question"),
    # url(r'^$', notices, name="notification_notices"),
    # url(r'^settings/$', notice_settings, name="notification_notice_settings"),
    # url(r'^(\d+)/$', single, name="notification_notice"),
    # url(r'^feed/$', feed_for_user, name="notification_feed_for_user"),
    # url(r'^mark_all_seen/$', mark_all_seen, name="notification_mark_all_seen"),
)
