from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns



urlpatterns = patterns('news.views',
                       url(r'^(?P<item_id>\d+)/$', 'news_item', name='news_item')
                       )

