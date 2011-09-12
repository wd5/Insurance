from django.conf.urls.defaults import *

urlpatterns = patterns('newcalc.views',
    url(r'^$', "step1", name='ncalc_step1'),
    # AJAX.
    url(r'^get_models/$', 'get_models', name="get_models"),
    url(r'^get_years/$', 'get_years', name="get_years"),
    url(r'^get_powers/$', 'get_powers', name="get_powers"),
)
