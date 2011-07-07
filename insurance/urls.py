from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.contrib import admin

import settings



admin.autodiscover()

urlpatterns = patterns('',
    # A simple template to close the site just in case...
    # url(r'^$', direct_to_template, {'template':'undercon.html'}),
    url(r'^$', direct_to_template, {'template':'index.html'}, name='home'),

    url(r'^accounts/', include('email_login.urls')),
    url(r'^profile/', include('profile.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                            {'document_root': settings.MEDIA_ROOT}
                         ),
    )
