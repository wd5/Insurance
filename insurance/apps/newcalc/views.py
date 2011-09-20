# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.utils import simplejson
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings

import socket
import urllib
import urllib2

from models import Mark, Model, Mym, ModelYear, Power, City, Price, BurglarAlarm
from forms import Step1Form, Step2Form

socket.setdefaulttimeout(settings.SERVLET_TIMEOUT)

S1_REQUIRED_KEYS = (
    "mark", "model", "model_year", "power", "price", "wheel", "city", "credit",
    "age", "experience_driving")


def step1(request):
    if request.method == "POST":
        form = Step1Form(request.POST, form_extra_data={})
        if form.is_valid():
            request.session["s1_data"] = _read_s1_data(form.cleaned_data)
            return redirect(reverse('ncalc_step2'))
    else:
        initial_data = {}
        form_extra_data = {}
        s1_data = request.session.get("s1_data")
        if s1_data:
            form_extra_data, initial_data = _read_form_data(s1_data)
        form = Step1Form(form_extra_data=form_extra_data, initial=initial_data)
    return direct_to_template(request, 'calc/step1.html', {"s1_form": form, })


def step2(request):
    """
    TODO:
    - валидация данных s1_data из сессии?
    """
    s1_data = request.session.get("s1_data")
    if not s1_data:
        return redirect(reverse('ncalc_step1'))
    for k in S1_REQUIRED_KEYS:
        if not s1_data.has_key(k):
            return redirect(reverse('ncalc_step1'))
    if s1_data["credit"]:
        credit_str = "on"
    else:
        credit_str = ""
    servlet_request_data = {"insurance_type": 1,
                            "mark": s1_data["mark"],
                            "model": s1_data["model"],
                            "model_year": s1_data["model_year"],
                            "power": s1_data["power"],
                            "price": s1_data["price"],
                            "wheel": s1_data["wheel"],
                            "city": s1_data["city"],
                            "credit": credit_str,
                            "age_0": s1_data["age"],
                            "experience_driving_0": s1_data[
                                                    "experience_driving"],
                            }
    s2_data = request.session.get("s2_data")
    if s2_data:
        for key in s2_data:
            if s2_data[key] == True:
                servlet_request_data[key] = "on"
            else:
                servlet_request_data[key] = s2_data[key]
    result = servlet_request(servlet_request_data)
    msg = None  # Some error message.
    if result is None:
        msg = "Не удалось получить данные от сервлета"
    else:
        try:
            result = simplejson.loads(result)
        except ValueError:
            msg = "Сервлет выдал в ответе не json, а фиг знает что"
        else:
            if result["status"] != "OK":
                msg = "Сервлет сообщил об ошибке"
    if request.method == "POST":
        form = Step2Form(request.POST, form_extra_data={})
        if form.is_valid():
            cd = form.cleaned_data
            s2_data = {}
            for key in cd:
                if key.startswith("factor_") and cd[key]:
                    s2_data[key] = True
            if cd["franchise"] is not None:  # Integer.
                s2_data["franchise"] = cd["franchise"]
            if cd["burglar_alarm_group"]:
                burglar_alarm_group = cd["burglar_alarm_group"]
                if not burglar_alarm_group.models.all().count():
                    s2_data["burglar_alarm"] = burglar_alarm_group.pk
                else:
                    s2_data["burglar_alarm"] = cd["burglar_alarm_model"].pk
            request.session["s2_data"] = s2_data

            return redirect(reverse('ncalc_step2'))
    else:
        initial_data = {}
        form_extra_data = {}
        if s2_data:
            for key in s2_data:
                if key.startswith("factor_"):
                    initial_data[key] = s2_data[key]
            if s2_data.has_key("franchise"):
                initial_data["franchise"] = s2_data["franchise"]
            if s2_data.has_key("burglar_alarm"):
                burglar_alarm = BurglarAlarm.objects.get(pk=s2_data["burglar_alarm"])
                if burglar_alarm.models.all().count():
                    initial_data["burglar_alarm_group"] = burglar_alarm
                else:
                    initial_data["burglar_alarm_group"] = burglar_alarm.burglar_alarm_parent
                    initial_data["burglar_alarm_model"] = burglar_alarm
                    form_extra_data["burglar_alarm_group"] = burglar_alarm.burglar_alarm_parent

        form = Step2Form(form_extra_data=form_extra_data, initial=initial_data)

    return direct_to_template(request, 'calc/step2.html', {"msg": msg, "s1_form": form,
                                                           "result": result})


def _read_s1_data(cd):
    s1_data = {}
    s1_data["mark"] = cd["mark"].pk
    s1_data["model"] = cd["model"].pk
    # s1_data["model_year"] = cd["model_year"]
    s1_data["model_year"] = Mym.objects.get(mym_y=cd["model_year"], mym_m=cd["model"]).mym_id
    s1_data["power"] = cd["power"].pk
    s1_data["price"] = cd["price"]
    s1_data["wheel"] = cd["wheel"]  # String.
    s1_data["city"] = cd["city"].pk
    s1_data["credit"] = cd["credit"]  # Bool.
    s1_data["age"] = int(cd["age"])
    s1_data["experience_driving"] = int(cd["experience_driving"])
    return s1_data


def _read_form_data(s1_data):
    initial_data = {}
    form_extra_data = {}
    ok = True

    if ok:
        try:
            mark = Mark.objects.get(pk=s1_data.get("mark"))
            initial_data["mark"] = mark
            form_extra_data["mark"] = mark
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            model = Model.objects.get(pk=s1_data.get("model"))
            initial_data["model"] = model
            form_extra_data["model"] = model
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            # model_year = ModelYear.objects.get(pk=s1_data.get("model_year"))
            model_year = Mym.objects.get(pk=s1_data.get("model_year")).mym_y
            initial_data["model_year"] = model_year
            form_extra_data["model_year"] = model_year
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            power = Power.objects.get(pk=s1_data.get("power"))
            initial_data["power"] = power
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            price = s1_data["price"]
            initial_data["price"] = price
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            wheel = s1_data["wheel"]
            initial_data["wheel"] = wheel
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            city = City.objects.get(pk=s1_data.get("city"))
            initial_data["city"] = city
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            credit = s1_data["credit"]
            initial_data["credit"] = credit
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            age = s1_data["age"]
            initial_data["age"] = age
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            experience_driving = s1_data["experience_driving"]
            initial_data["experience_driving"] = experience_driving
        except (ObjectDoesNotExist, KeyError):
            ok = False

    return form_extra_data, initial_data


def servlet_request(data):
    result = None
    if settings.SERVLET_FAKE:
        result_dict = {'status': 'OK', 'info':
                     [{'full_name': 'TestCompany-1',
                     'parameters': {'Evacuator': 'on',
                         'TheEmergencyCommissioner': 'on',
                         'PaymentWithoutInquiries': 'on',
                         'GatheringOfInquiries': 'on',
                         'TheModularInsuranceSum': 'on',
                         'NewForTheOld': 'on',
                         'TheObligatoryFranchize': 'on',
                         'AlternativenessOfFormsOfPayment': 'on',
                         }},
                    {'full_name': 'TestCompany-2',
                     'parameters': {'Evacuator': 'on',
                                    'TheEmergencyCommissioner': '',
                                    'PaymentWithoutInquiries': 'on',
                                    'GatheringOfInquiries': '',
                                    'TheModularInsuranceSum': 'on',
                                    'NewForTheOld': '',
                                    'TheObligatoryFranchize': 'on',
                                    'AlternativenessOfFormsOfPayment': '',
                                    }},
                    {'full_name': 'TestCompany-3',
                     'parameters': {'Evacuator': '',
                                    'TheEmergencyCommissioner': 'on',
                                    'PaymentWithoutInquiries': '',
                                    'GatheringOfInquiries': 'on',
                                    'TheModularInsuranceSum': '',
                                    'NewForTheOld': 'on',
                                    'TheObligatoryFranchize': '',
                                    'AlternativenessOfFormsOfPayment': 'on',
                                    }}]
                     }
        result = simplejson.dumps(result_dict)
    else:
        encoded_data = urllib.urlencode(data)
        # print "REQUEST:", encoded_data
        req = urllib2.Request(settings.SERVLET_URL, encoded_data)
        # print "REQUEST:", req
        try:
            result = urllib2.urlopen(req).read()
            # print "RESULT: ", result
        except socket.timeout:
            pass
    return result


# AJAX.
@require_GET
def get_models(request):
    response_dict = {}
    if request.is_ajax() and request.GET.has_key("mark"):
        try:
            mark = Mark.objects.get(pk=request.GET["mark"])
        except ObjectDoesNotExist:
            pass
        else:
            models = mark.model_set.all()
            for model in models:
                response_dict[model.model_id] = model.model_name
    response = simplejson.dumps(response_dict)
    return HttpResponse(response, mimetype='application/javascript')


@require_GET
def get_years(request):
    response_dict = {}
    if request.is_ajax() and request.GET.has_key("model"):
        try:
            mym = Mym.objects.filter(mym_m=request.GET["model"])
        except ObjectDoesNotExist, e:
            print e
        else:
            years = [m.mym_y for m in mym]
            for year in years:
                response_dict[year.year_id] = year.model_year_year
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
