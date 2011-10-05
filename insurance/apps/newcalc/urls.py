from django.conf.urls.defaults import *

urlpatterns = patterns('newcalc.views',
    url(r'^$', "step1", name='ncalc_step1'),
    url(r'^step2/$', "step2", name='ncalc_step2'),
    url(r'^step3/(\w+)/$', "step3", name='ncalc_step3'),
    url(r'^step4/$', "step4", name='ncalc_step4'),
    url(r'^cleansession/$', "cleansession", name='cleansession'),
    # AJAX.
    url(r'^get_models/$', 'get_models', name="get_models"),
    url(r'^get_years/$', 'get_years', name="get_years"),
    url(r'^get_powers/$', 'get_powers', name="get_powers"),
    url(r'^get_price/$', 'get_price', name="get_price"),
    url(r'^get_ba_models/$', 'get_ba_models', name="get_ba_models"),
    url(r'^get_person_address/$', 'get_person_address', name="get_person_address"),
)
