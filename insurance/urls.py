from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from django.conf import settings

from index import home


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),

    url(r'^accounts/', include('email_login.urls')),
    url(r'^profile/', include('profile.urls')),
    #url(r'^profile/messages/', include('django_messages.urls')),
    url(r'^messages/', include('notification.urls')),
    url(r'^notification/', include('ins_notification.urls')),
    url(r'^calc/', include('calc.urls')),
    url(r'^newcalc/', include('newcalc.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                            {'document_root': settings.MEDIA_ROOT}
                         ),
    )
