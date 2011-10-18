from django.conf.urls.defaults import *

urlpatterns = patterns('newcalc.views',
    url(r'^$', "index", name="ncalc_index"),
    #url(r'^step4/(?P<step>\d+)/$', "step4", name='ncalc_step4'),
    url(r'^cleansession/$', "cleansession", name='cleansession'),
    # AJAX.
    url(r'^get_models/$', 'get_models', name="get_models"),
    url(r'^get_years/$', 'get_years', name="get_years"),
    url(r'^get_powers/$', 'get_powers', name="get_powers"),
    url(r'^get_price/$', 'get_price', name="get_price"),
    url(r'^get_ba_models/$', 'get_ba_models', name="get_ba_models"),
    url(r'^get_person_address/$', 'get_person_address', name="get_person_address"),
)

urlpatterns += patterns('newcalc.calcs.kasko',
    url(r'^kasko/$', "step1", name='ncalc_step1_kasko'),
    url(r'^kasko/step2/$', "step2", name='ncalc_step2_kasko'),
    url(r'^kasko/step3/(\w+)/$', "step3", name='ncalc_step3_kasko'),
    url(r'^kasko/step4/$', "step4", name='ncalc_step4_kasko'),
)

urlpatterns += patterns('newcalc.calcs.osago',
    url(r'^osago/$', "step1", name='ncalc_step1_osago'),
    url(r'^osago/step2/$', "step2", name='ncalc_step2_osago'),
    url(r'^osago/step3/(\w+)/$', "step3", name='ncalc_step3_osago'),
    url(r'^osago/step4/$', "step4", name='ncalc_step4_osago'),
)
