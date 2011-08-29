# -*- coding: utf-8 -*-
import sys
from calc.utils_db import get_power_by_model_and_year,get_price_by_model_and_power
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect

def power(request,mym_id=''):
    result = get_power_by_model_and_year(mym_id)
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')

def price(request,price_mym='',price_power=''):
    result = get_price_by_model_and_power(price_mym,price_power)
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')
