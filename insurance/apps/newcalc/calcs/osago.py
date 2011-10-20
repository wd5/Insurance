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

from newcalc.models import Mark, Model, Mym, Power, City,\
    BurglarAlarm, Company, CompanyCondition, InsuranceType, \
    KackoParameters
from newcalc.forms.osago import Step1Form, Step2Form, Step3FormReg, Step3FormNoReg
from newcalc.forms.osago import Step4Form
from polices.forms import CallRequestForm
from profile.models import Persona
from polices.models import InsurancePolicy #, CallRequests
from email_login.backends import RegistrationBackend
from newcalc.servlet import servlet_request


socket.setdefaulttimeout(settings.SERVLET_TIMEOUT)


# ========== General views ==========

S1_REQUIRED_KEYS = (
    "mark", "model", "model_year", "power", "dago",
    "violations", "city", "age", "experience_driving")


def step1(request):
    if request.method == "POST":
        form = Step1Form(request.POST, form_extra_data={})
        if form.is_valid():
            request.session["s1_data_osago"] = _s1_read_data(form.cleaned_data)
            return redirect(reverse('ncalc_step2_osago'))
    else:
        initial_data = {}
        form_extra_data = {}
        s1_data = request.session.get("s1_data_osago")
        if s1_data:
            form_extra_data, initial_data = _s1_read_form_data(s1_data)
        else:
            initial_data['dago'] = 0
        form = Step1Form(form_extra_data=form_extra_data, initial=initial_data)
    return direct_to_template(request, 'calc/osago/step1.html', {"s1_form": form, 'tab': 2})


def step2(request):
    """
    TODO:
    - валидация данных s1_data из сессии?
    """
    s1_data = request.session.get("s1_data_osago")
    s2_data = request.session.get("s2_data_osago")

    if not s1_data:
        return redirect(reverse('ncalc_step1_osago'))
    for k in S1_REQUIRED_KEYS:
        if not s1_data.has_key(k):
            return redirect(reverse('ncalc_step1_osago'))
    if not s2_data:
        s2_data = dict()
        s2_data['factor_reputation'] = True #Если нет данных => только перешли ко 2 шагу - сортируем по репутации
    result = servlet_request(_build_servlet_request_data(s1_data, s2_data), servlet_type="osago")
    if result is None:
        err_text = "Превышен лимит ожидания. Не получен ответ сервлета в "\
                   "течение %d сек." % settings.SERVLET_TIMEOUT
        return direct_to_template(request, "calc/error.html", {"err_text": err_text, 'tab': 2})

    result, msg = _parse_servlet_response(result)

    data = {}
    data["mark"] = Mark.objects.get(pk=s1_data["mark"]).mark_name
    data["model"] = Model.objects.get(pk=s1_data["model"]).model_name
    data["model_year"] = Mym.objects.get(pk=s1_data["model_year"]).mym_y.model_year_year

    if request.method == "POST":
        form = Step2Form(request.POST)
        if form.is_valid():
            request.session["s2_data_osago"] = _s2_read_data(form.cleaned_data)
            return redirect(reverse('ncalc_step2_osago'))
    else:
        initial_data = _s2_read_form_data(s2_data)
        form = Step2Form(initial=initial_data)
    table = KackoParameters.objects.filter(is_active=True)
    header = dict()
    for t in table:
        header[t.kparameter_alias] = {'name':t.kparameter_name, 'comment':t.kparameter_comment}
    return direct_to_template(request, 'calc/osago/step2.html', {"msg": msg,
                                                                 "s1_form": form,
                                                                 "result": result,
                                                                 "header":header,
                                                                 "data": data, 'tab': 2})


def step3(request, alias):
    call_form = CallRequestForm()
    s1_data = request.session.get("s1_data_osago")
    if not s1_data:
        return redirect(reverse('ncalc_step1_osago'))

    data = {}
    data["insurance_type"] = "ОСАГО"
    if str(s1_data["violations"]) == "1":
        data["violations"] = "не было"
    else:
        data["violations"] = "были"
    data["mark"] = Mark.objects.get(pk=s1_data["mark"]).mark_name
    data["model"] = Model.objects.get(pk=s1_data["model"]).model_name
    data["model_year"] = Mym.objects.get(pk=s1_data["model_year"]).mym_y.model_year_year
    data["power"] = Power.objects.get(pk=s1_data["power"]).power_name
    data["dago"] = s1_data["dago"]
    data["city"] = City.objects.get(pk=s1_data["city"]).city_name

    data["age"] = s1_data["age"]
    data["experience_driving"] = s1_data["experience_driving"]

    data["company"] = Company.objects.get(company_alias=alias).company_name

    if s1_data["unlimited_drivers"]:
        data["dr_nr"] = "не ограничено"
    else:
        if s1_data.has_key("age3"):
            data["dr_nr"] = "4"
        elif s1_data.has_key("age2"):
            data["dr_nr"] = "3"
        elif s1_data.has_key("age1"):
            data["dr_nr"] = "2"
        else:
            data["dr_nr"] = "1"

    if request.method == "POST":
        if request.user.is_authenticated():
            form = Step3FormReg(request.POST)
            if form.is_valid():
                request.session["company_alias"] = alias
                ip = InsurancePolicy()
                ip.user = request.user
                ip.type = 2
                ip.company = Company.objects.get(company_alias=alias).company_full_name
                ip.mark = Mark.objects.get(pk=s1_data["mark"]).mark_name
                ip.model = Model.objects.get(pk=s1_data["model"]).model_name
                ip.model_year = Mym.objects.get(pk=s1_data["model_year"]).mym_y.model_year_year
                ip.power = Power.objects.get(pk=s1_data["power"]).power_name
                ip.city = City.objects.get(pk=s1_data["city"]).city_name
                ip.price = 0  # N/A
                ip.age = s1_data["age"]
                ip.experience_driving = s1_data["experience_driving"]
                if s1_data["unlimited_drivers"]:
                    ip.unlimited_users = True
                else:
                    ip.unlimited_users = False
                    if s1_data.has_key("age1"):
                        ip.age1 = s1_data["age1"]
                        ip.experience_driving1 = s1_data["experience_driving1"]
                    if s1_data.has_key("age2"):
                        ip.age2 = s1_data["age2"]
                        ip.experience_driving2 = s1_data["experience_driving2"]
                    if s1_data.has_key("age3"):
                        ip.age3 = s1_data["age3"]
                        ip.experience_driving3 = s1_data["experience_driving3"]
                policy = ip.save()
                request.session['policy'] = ip.pk

                return redirect(reverse('ncalc_step4_osago'))
        else:
            form = Step3FormNoReg(request.POST)
            if form.is_valid():
                new_user = RegistrationBackend().register(request,
                                                          **form.cleaned_data)
                request.session["new_user"] = new_user.pk
                ip = InsurancePolicy()
                ip.type = 2
                ip.user = new_user
                ip.company = Company.objects.get(company_alias=alias).company_full_name
                ip.mark = Mark.objects.get(pk=s1_data["mark"]).mark_name
                ip.model = Model.objects.get(pk=s1_data["model"]).model_name
                ip.model_year = Mym.objects.get(pk=s1_data["model_year"]).mym_y.model_year_year
                ip.power = Power.objects.get(pk=s1_data["power"]).power_name
                ip.city = City.objects.get(pk=s1_data["city"]).city_name
                ip.price = 0  # N/A
                ip.age = s1_data["age"]
                ip.experience_driving = s1_data["experience_driving"]
                if s1_data["unlimited_drivers"]:
                    ip.unlimited_users = True
                else:
                    ip.unlimited_users = False
                    if s1_data.has_key("age1"):
                        ip.age1 = s1_data["age1"]
                        ip.experience_driving1 = s1_data["experience_driving1"]
                    if s1_data.has_key("age2"):
                        ip.age2 = s1_data["age2"]
                        ip.experience_driving2 = s1_data["experience_driving2"]
                    if s1_data.has_key("age3"):
                        ip.age3 = s1_data["age3"]
                        ip.experience_driving3 = s1_data["experience_driving3"]
                policy = ip.save()
                request.session['policy'] = ip.pk
                request.session["company_alias"] = alias
                return redirect(reverse('ncalc_step4_osago'))
    else:
        if request.user.is_authenticated():
            form = Step3FormReg()
        else:
            form = Step3FormNoReg()
    if request.user.is_authenticated():
        return direct_to_template(request, 'calc/osago/step3reg.html', {"data": data, "form": form, "call_form":call_form, 'tab': 2})
    else:
        return direct_to_template(request, 'calc/osago/step3noreg.html', {"data": data, "form": form, "call_form":call_form, 'tab': 2})

def step4(request):
    policy_id = request.session.get('policy')
    if not policy_id:
        #policy_id = 1 #для показа
        return redirect(reverse('ncalc_step1_osago')) #, args=[request.session.get('company_alias')]))
    policy = InsurancePolicy.objects.get(pk=policy_id)
    if request.method == 'POST':
        form = Step4Form(request.POST)
        if form.is_valid():
            policy_data = form.save(commit=False)
            policy_data.polisy = policy
            policy_data.save()
            #return redirect(reverse('ncalc_success'))

    initial_data = {}
#    if request.user.is_authenticated() or policy:
#TODO: возможно несколько персон у одного юзера - учесть это
    persona = Persona.objects.filter(user=policy.user)[0]
    #initial_data['power'] = policy.power
    initial_data['first_name'] = persona.first_name
    initial_data['last_name'] = persona.last_name
    initial_data['middle_name'] = persona.middle_name

    form = Step4Form(initial=initial_data)
    return direct_to_template(request, 'calc/osago/step4.html', {"form": form, 'tab': 2})

# ========== Auxilary ==========


def _s1_read_data(cd):
    s1_data = {}
    s1_data["mark"] = cd["mark"].pk
    s1_data["model"] = cd["model"].pk
    s1_data["model_year"] = Mym.objects.get(mym_y=cd["model_year"],
                                            mym_m=cd["model"]).mym_id
    s1_data["power"] = cd["power"].pk
    s1_data["dago"] = cd["dago"]
    s1_data["violations"] = cd["violations"]  # String.
    s1_data["city"] = cd["city"].pk
    s1_data["age"] = int(cd["age"])
    s1_data["experience_driving"] = int(cd["experience_driving"])
    unlimited_drivers = cd["unlimited_drivers"]
    if unlimited_drivers:
        s1_data["unlimited_drivers"] = 1
    else:
        s1_data["unlimited_drivers"] = 0
        if cd["age1"]:
            s1_data["age1"] = int(cd["age1"])
            s1_data["experience_driving1"] = int(cd["experience_driving1"])
        if cd["age2"]:
            s1_data["age2"] = int(cd["age2"])
            s1_data["experience_driving2"] = int(cd["experience_driving2"])
        if cd["age3"]:
            s1_data["age3"] = int(cd["age3"])
            s1_data["experience_driving3"] = int(cd["experience_driving3"])
    return s1_data


def _s1_read_form_data(s1_data):
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
            model = Model.objects.filter(pk=s1_data.get("model"), model_active=1)
            initial_data["model"] = model[0]
            form_extra_data["model"] = model[0]
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
            price = s1_data["dago"]
            initial_data["dago"] = price
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            wheel = s1_data["violations"]
            initial_data["violations"] = wheel
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
    if ok:
        try:
            unlimited_drivers = s1_data["unlimited_drivers"]
            initial_data["unlimited_drivers"] = bool(unlimited_drivers)
        except KeyError:
            ok = False
    if ok:
        try:
            age1 = s1_data["age1"]
            experience_driving1 = s1_data["experience_driving1"]
            initial_data["age1"] = age1
            initial_data["experience_driving1"] = experience_driving1
        except KeyError:
            ok = False
    if ok:
        try:
            age2 = s1_data["age2"]
            experience_driving2 = s1_data["experience_driving2"]
            initial_data["age2"] = age2
            initial_data["experience_driving2"] = experience_driving2
        except KeyError:
            ok = False
    if ok:
        try:
            age3 = s1_data["age3"]
            experience_driving3 = s1_data["experience_driving3"]
            initial_data["age3"] = age3
            initial_data["experience_driving3"] = experience_driving3
        except KeyError:
            ok = False
    return form_extra_data, initial_data


def _s2_read_data(cd):
    s2_data = {}
    for key in cd:
        if key.startswith("factor_") and cd[key]:
            s2_data[key] = True
    return s2_data


def _s2_read_form_data(s2_data):
    initial_data = {}
    if s2_data:
        for key in s2_data:
            if key.startswith("factor_"):
                initial_data[key] = s2_data[key]
    return initial_data


def _build_servlet_request_data(s1_data, s2_data):
    unlimited_drivers = s1_data.get("unlimited_drivers")
    if unlimited_drivers is None:
        unlimited_drivers = 0

    servlet_request_data = {"power": s1_data["power"],
                            "infringement": s1_data["violations"],
                            "city": s1_data["city"],
                            "age_0": s1_data["age"],
                            "experience_driving_0": s1_data["experience_driving"],
#                            "unlimited_drivers": unlimited_drivers,
                            }
    if s1_data.has_key("age1"):
        servlet_request_data["age_1"] = s1_data["age1"]
        servlet_request_data["experience_driving_1"] =\
            s1_data["experience_driving1"]
    if s1_data.has_key("age2"):
        servlet_request_data["age_2"] = s1_data["age2"]
        servlet_request_data["experience_driving_2"] =\
            s1_data["experience_driving2"]
    if s1_data.has_key("age3"):
        servlet_request_data["age_3"] = s1_data["age3"]
        servlet_request_data["experience_driving_3"] =\
            s1_data["experience_driving3"]
    if s2_data:
        for key in s2_data:
            if s2_data[key] == True:
                servlet_request_data[key] = "on"
            else:
                servlet_request_data[key] = s2_data[key]
    return servlet_request_data

def _parse_servlet_response(result):
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
            else:
                for company in result['info']:
                    company_id = Company.objects.get(company_alias = company['alias']).company_id
                    comment = CompanyCondition.objects.filter(company_condition_company = company_id,
                                                              company_condition_insurance = 2)
                    if comment:
                        company['company_comment'] = comment[0].company_condition_comment
                    else:
                        company['company_comment'] = ''
    return result, msg
