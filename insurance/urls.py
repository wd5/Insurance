from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.contrib import admin

import settings



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'insurance.views.home', name='home'),
    # url(r'^insurance/', include('insurance.foo.urls')),

    url(r'^$', direct_to_template, {'template':'index.html'}, name='site_root'),

    (r'^accounts/', include('registration.backends.default.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                            {'document_root': settings.MEDIA_ROOT}
                         ),
    )
