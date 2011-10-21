# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.utils import simplejson
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string

import socket

from models import Mark, Model, Mym, ModelYear, Power, City,\
    BurglarAlarm, Company, CompanyCondition, InsuranceType, \
    KackoParameters
from polices.forms import CallRequestForm
from profile.models import Persona
from polices.models import InsurancePolicy #, CallRequests
from email_login.backends import RegistrationBackend
from servlet import servlet_request


def index(request):
    return redirect(reverse("ncalc_step1_kasko"))

# ========== General views ==========

socket.setdefaulttimeout(settings.SERVLET_TIMEOUT)

def cleansession(request):
    """
    Вьюха, созданная для использования во время тестирования
    для очистки данных сессии.
    """
    request.session.clear()
    return redirect(reverse('ncalc_index'))

def success(request):
    return direct_to_template(request, 'calc/success.html')

# ========== AJAX ==========


@require_GET
def get_models(request):
    response_dict = {}
    if request.is_ajax() and request.GET.has_key("mark"):
        try:
            mark = Mark.objects.get(pk=request.GET["mark"])
        except ObjectDoesNotExist:
            pass
        else:
            models = mark.model_set.filter(model_active=1)
            for model in models:
                response_dict[model.model_id] = model.model_name
    response = simplejson.dumps(response_dict)
    return HttpResponse(response, mimetype='application/javascript')


@require_GET
def get_years(request):
    years = ModelYear.objects.order_by("model_year_year")
    response_dict = dict([(x.year_id, x.model_year_year) for x in years])
#    if request.is_ajax() and request.GET.has_key("model"):
#        try:
#            mym = Mym.objects.filter(mym_m=request.GET["model"])
#        except ObjectDoesNotExist, e:
#            print e
#        else:
#            years = [m.mym_y for m in mym]
#            for year in years:
#                response_dict[year.year_id] = year.model_year_year
    response = simplejson.dumps(response_dict)
    return HttpResponse(response, mimetype='application/javascript')


@require_GET
def get_powers(request):
    response_dict = {}
    if request.is_ajax() and request.GET.has_key("model") and\
       request.GET.has_key("year"):
        # COMMENT: временное упрощение
        # try:
        #     mym = Mym.objects.get(mym_y=request.GET["year"],
        #                           mym_m=request.GET["model"])
        # except ObjectDoesNotExist:
        #     pass
        # else:
        #     powers = mym.power_set.all()
        #     for power in powers:
        #         response_dict[power.power_id] = power.power_name
        powers = Power.objects.all()
        for power in powers:
            response_dict[power.power_id] = power.power_name
    response = simplejson.dumps(response_dict)
    return HttpResponse(response, mimetype='application/javascript')


@require_GET
def get_price(request):
    response = ""
    if request.is_ajax() and request.GET.has_key("power"):
        # COMMENT: временное упрощение
        # try:
        #     power = Power.objects.get(pk=request.GET["power"])
        # except ObjectDoesNotExist:
        #     pass
        # else:
        #     try:
        #         price = Price.objects.get(price_power=power)
        #     except ObjectDoesNotExist:
        #         pass
        #     else:
        #         response = "от %d до %d" % (price.price_min, price.price_max)
        response = "от %d до %d" % (0, 1000000)
    return HttpResponse(response, mimetype='text/plain')


@require_GET
def get_ba_models(request):
    response_dict = {}
    if request.is_ajax() and request.GET.has_key("group"):
        try:
            mark = BurglarAlarm.objects.get(pk=request.GET["group"])
        except ObjectDoesNotExist:
            pass
        else:
            models = mark.models.all()
            for model in models:
                response_dict[model.burglar_alarm_id] = model.burglar_alarm_name
    response = simplejson.dumps(response_dict)
    return HttpResponse(response, mimetype='application/javascript')


@require_GET
def get_person_address(request):
    response = ""
    if request.is_ajax() and request.GET.has_key("pers"):
        try:
             persona = Persona.objects.get(pk=request.GET["pers"])
        except ObjectDoesNotExist:
             pass
        else:
             response = persona.get_full_address()
    return HttpResponse(response, mimetype='text/plain')
