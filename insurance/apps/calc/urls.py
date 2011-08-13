from django.conf.urls.defaults import *
from calc.views import calc_step_1,calc_step_2,calc_step_3

urlpatterns = patterns('',
                       url(r'calc_step_1/$',calc_step_1,name='calc_step_1'),
                       url(r'calc_step_2/$',calc_step_2,name='calc_step_2'),
                       url(r'calc_step_3/$',calc_step_3,name='calc_step_3 '),
                       url(r'calc/$',calc_step_1,name='calc_page'),
                       url(r'$',calc_step_1,name='calc_step_1'),
                       )
