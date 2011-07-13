from django.conf.urls.defaults import *
from calc.views import servlet_test

urlpatterns = patterns('',
                       url(r'servlet_test/$',servlet_test))
