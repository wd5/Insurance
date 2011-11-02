# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.utils import simplejson
from django.views.decorators.http import require_GET
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string

import socket

from newcalc.models import City, Company, CompanyCondition, InsuranceType, \
    PropertyParameters, Property
from newcalc.forms.ifl import Step1Form, Step2Form, Step3FormReg, Step3FormNoReg
from newcalc.forms.ifl import Step4Form, Step5Form, Step6Form
from polices.forms import CallRequestForm
from profile.models import Persona
from polices.models import InsurancePolicyIFL #, CallRequests
from email_login.backends import RegistrationBackend
from newcalc.servlet import servlet_request
from newcalc.templatetags.intspace import intspace

# ========== General views ==========

def success(request):
    request.session['policy_ifl'] = None
    return direct_to_template(request, 'calc/success.html', {'tab': 6})


S1_REQUIRED_KEYS = ("property", "property_sum", "city")


def step1(request, prev=0):
    if prev != 0:
        prev_int = int(prev)
        pr_data =  request.session.get("s1_data_ifl%d" % prev_int)
        curr_data =  request.session.get("s1_data_ifl")
        if pr_data is None:
            raise Http404
        if prev_int == 1:
            request.session["s1_data_ifl1"] = curr_data
            request.session["s1_data_ifl"] = pr_data
        else:  # 2.
            k1 =  request.session.get("s1_data_ifl1")
            request.session["s1_data_ifl2"] = k1
            request.session["s1_data_ifl1"] = curr_data
            request.session["s1_data_ifl"] = pr_data
        return redirect(reverse('ncalc_step1_ifl'))
    if request.method == "POST":
        form = Step1Form(request.POST)
        if form.is_valid():
            new_data = _s1_read_data(form.cleaned_data)
            k1 =  request.session.get("s1_data_ifl1")
            k0 =  request.session.get("s1_data_ifl")
            # Избегаем дублирования.
            if k0 and not (new_data["property"]==k0["property"]
                           and new_data["property_sum"]==k0["property_sum"]):
                if k1:
                    request.session["s1_data_ifl2"] = k1
                request.session["s1_data_ifl1"] = k0
            request.session["s1_data_ifl"] = new_data
            return redirect(reverse('ncalc_step2_ifl'))
    else:
        initial_data = {}
        form_extra_data = {}
        s1_data = request.session.get("s1_data_ifl")
        if s1_data:
            form_extra_data, initial_data = _s1_read_form_data(s1_data)
        else:
            initial_data['property_sum'] = 0
            initial_data['interior_decoration_summ'] = 0
            initial_data['environment_summ'] = 0
            initial_data['household_effects_summ'] = 0
            initial_data['civil_liability_summ'] = 0
        form = Step1Form(initial=initial_data)
    k1 =  request.session.get("s1_data_ifl1")
    k2 =  request.session.get("s1_data_ifl2")
    prev_data = []
    if k1:
        ptype = Property.objects.get(pk=k1["property"]).property_name
        price = k1["property_sum"]
        prev_data.append("%s / %s" % (ptype, intspace(price)))
    if k2:
        ptype = Property.objects.get(pk=k1["property"]).property_name
        price = k2["property_sum"]
        prev_data.append("%s / %s" % (ptype, intspace(price)))
    return direct_to_template(request, 'calc/ifl/step1.html', {"s1_form": form,
                                                               "prev_data": prev_data, 'tab': 6})


def step2(request):
    """
    TODO:
    - валидация данных s1_data из сессии?
    """
    s1_data = request.session.get("s1_data_ifl")
    s2_data = request.session.get("s2_data_ifl")

    if not s1_data:
        return redirect(reverse('ncalc_step1_ifl'))
    for k in S1_REQUIRED_KEYS:
        if not s1_data.has_key(k):
            return redirect(reverse('ncalc_step1_ifl'))
    if not s2_data:
        s2_data = dict()
        s2_data['factor_price'] = True #Если нет данных => только перешли ко 2 шагу - сортируем по репутации
    result = servlet_request(_build_servlet_request_data(s1_data, s2_data), servlet_type="ifl")
    if result is None:
        err_text = "Превышен лимит ожидания. Не получен ответ сервлета в "\
                   "течение %d сек." % settings.SERVLET_TIMEOUT
        return direct_to_template(request, "calc/error.html", {"err_text": err_text, 'tab': 6})

    result, msg = _parse_servlet_response(result)

    data = {}
    data["property"] = Property.objects.get(pk=s1_data["property"]).property_name
    data["property_sum"] = s1_data["property_sum"]

    if request.method == "POST":
        form = Step2Form(request.POST)
        if form.is_valid():
            request.session["s2_data_ifl"] = _s2_read_data(form.cleaned_data)
            return redirect(reverse('ncalc_step2_ifl'))
    else:
        form_extra_data, initial_data = _s2_read_form_data(s2_data)
        form = Step2Form(initial=initial_data)
    table = PropertyParameters.objects.filter(pparameter_active=True)
    header = dict()
    for t in table:
        header[t.pparameter_alias] = {'name':t.pparameter_name, 'comment':t.pparameter_comment}
    return direct_to_template(request, 'calc/ifl/step2.html', {"msg": msg, 'tab': 6,
                                                               "s1_form": form,
                                                               "result": result,
                                                               "header":header,
                                                               "data": data})


def step3(request, alias):
    call_form = CallRequestForm()
    s1_data = request.session.get("s1_data_ifl")
    if not s1_data:
        return redirect(reverse('ncalc_step1_ifl'))
    data = {}
    data["insurance_type"] = "ИФЛ"
    data["property"] = Property.objects.get(pk=s1_data["property"]).property_name
    data["property_sum"] = s1_data["property_sum"]
    data["city"] = City.objects.get(pk=s1_data["city"]).city_name
    data["company"] = Company.objects.get(company_alias=alias).company_name
    if s1_data.get("interior_decoration", False):
        data["interior_sum"] = s1_data["interior_decoration_summ"]
    if s1_data.get("environment", False):
        data["environment_sum"] = s1_data["environment_summ"]
    if s1_data.get("household_effects", False):
        data["household_sum"] = s1_data["household_effects_summ"]
    if s1_data.get("civil_liability", False):
        data["civil_sum"] = s1_data["civil_liability_summ"]
    if request.method == "POST":
        if request.user.is_authenticated():
            form = Step3FormReg(request.POST)
            if form.is_valid():
                request.session["company_alias"] = alias
                ip = InsurancePolicyIFL()
                ip.user = request.user
                ip.company = Company.objects.get(company_alias=alias).company_full_name

                ip.property = Property.objects.get(pk=s1_data["property"]).property_name
                ip.property_sum = s1_data["property_sum"]
                ip.city = City.objects.get(pk=s1_data["city"]).city_name

                ip.interior_decoration = s1_data.get("interior_decoration_summ", 0)
                ip.environment = s1_data.get("environment_summ", 0)
                ip.household_effects = s1_data.get("household_effects_summ", 0)
                ip.civil_liability = s1_data.get("civil_liability_summ", 0)
                policy = ip.save()
                request.session['policy_ifl'] = ip.pk

                return redirect(reverse('ncalc_step4_ifl'))
        else:
            form = Step3FormNoReg(request.POST)
            if form.is_valid():
                new_user = RegistrationBackend().register(request,
                                                          **form.cleaned_data)
                request.session["new_user"] = new_user.pk
                ip = InsurancePolicyIFL()
                ip.user = new_user

                ip.company = Company.objects.get(company_alias=alias).company_full_name

                ip.property = Property.objects.get(pk=s1_data["property"]).property_name
                ip.property_sum = s1_data["property_sum"]
                ip.city = City.objects.get(pk=s1_data["city"]).city_name

                ip.interior_decoration = s1_data.get("interior_decoration_summ", 0)
                ip.environment = s1_data.get("environment_summ", 0)
                ip.household_effects = s1_data.get("household_effects_summ", 0)
                ip.civil_liability = s1_data.get("civil_liability_summ", 0)

                policy = ip.save()
                request.session['policy_ifl'] = ip.pk
                request.session["company_alias"] = alias
                return redirect(reverse('ncalc_step4_ifl'))
    else:
        if request.user.is_authenticated():
            form = Step3FormReg()
        else:
            form = Step3FormNoReg()
    if request.user.is_authenticated():
        return direct_to_template(request, 'calc/ifl/step3reg.html', {"data": data, "form": form, "call_form":call_form, 'tab': 6})
    else:
        return direct_to_template(request, 'calc/ifl/step3noreg.html', {"data": data, "form": form, "call_form":call_form, 'tab': 6})

def step4(request):
    policy_id = request.session.get('policy_ifl')
    if not policy_id:
        return redirect(reverse('ncalc_step1_ifl')) #, args=[request.session.get('company_alias')]))
    policy = InsurancePolicyIFL.objects.get(pk=policy_id)
    policy_data = InsurancePolicyIFL.objects.values().get(pk=policy_id)
    if request.method == 'POST':
        form = Step4Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for k in cd.keys():
                if cd[k]:
                    setattr(policy, k, cd[k])
            policy.save()
            return redirect(reverse('ncalc_step5_ifl'))
    else:
        initial_data = {}
        #TODO: сделать возможность добавления данных по др. водителям.
        #TODO: здесь расширить список данных, получаемых из персоны.
        persona = Persona.objects.get(user=policy.user, me=True)
        if not policy.first_name or not policy.last_name or not policy.middle_name:
            initial_data['first_name'] = persona.first_name
            initial_data['last_name'] = persona.last_name
            initial_data['middle_name'] = persona.middle_name
            form = Step4Form(initial=initial_data)
        else:
            form = Step4Form(initial=policy_data)
    return direct_to_template(request, 'calc/ifl/step4.html', {"form": form, 'tab': 6})


def step5(request):
    policy_id = request.session.get('policy_ifl')
    if not policy_id:
        return redirect(reverse('ncalc_step1_ifl')) #, args=[request.session.get('company_alias')]))
    policy = InsurancePolicyIFL.objects.get(pk=policy_id)
    policy_data = InsurancePolicyIFL.objects.values().get(pk=policy_id)

    if request.method == 'POST':
        form = Step5Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for k in cd.keys():
                if cd[k]:
                    setattr(policy, k, cd[k])
            policy.save()
            return redirect(reverse('ncalc_step6_ifl'))
    else:
        form = Step5Form(initial=policy_data)

    copy = {"first_name": policy.first_name,
            "middle_name": policy.middle_name,
            "last_name": policy.last_name,
            "birth_date": policy.birth_date.strftime("%d.%m.%Y"),
            "sex": policy.sex}
    return direct_to_template(request, 'calc/ifl/step5.html', {"form": form, "tab": 6,
                                                               "copy": copy,
                                                               "back": reverse("ncalc_step4_ifl")})

def step6(request):
    policy_id = request.session.get('policy_ifl')
    if not policy_id:
        return redirect(reverse('ncalc_step1_ifl')) #, args=[request.session.get('company_alias')]))
    policy = InsurancePolicyIFL.objects.get(pk=policy_id)
    policy_data = InsurancePolicyIFL.objects.values().get(pk=policy_id)

    if request.method == 'POST':
        form = Step6Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for k in cd.keys():
                if cd[k]:
                    setattr(policy, k, cd[k])
            policy.save()
            return redirect(reverse('ncalc_success_ifl'))
    else:
        form = Step6Form(initial=policy_data)
    return direct_to_template(request, 'calc/ifl/step6.html', {"form": form, 'tab': 6,
                                                               "back": reverse("ncalc_step5_ifl")})

# ========== Auxilary ==========


def _s1_read_data(cd):
    s1_data = {}
    s1_data["property"] = cd["property"].pk
    s1_data["property_sum"] = int(cd["property_sum"])
    s1_data["city"] = cd["city"].pk

    if cd["interior_decoration"]:
        s1_data["interior_decoration"] = True
        s1_data["interior_decoration_summ"] = int(cd["interior_decoration_summ"])

    if cd["environment"]:
        s1_data["environment"] = True
        s1_data["environment_summ"] = int(cd["environment_summ"])

    if cd["household_effects"]:
        s1_data["household_effects"] = True
        s1_data["household_effects_summ"] = int(cd["household_effects_summ"])

    if cd["civil_liability"]:
        s1_data["civil_liability"] = True
        s1_data["civil_liability_summ"] = int(cd["civil_liability_summ"])

    return s1_data


def _s1_read_form_data(s1_data):
    initial_data = {}
    form_extra_data = {}
    ok = True

    if ok:
        try:
            property = Property.objects.get(pk=s1_data.get("property"))
            initial_data["property"] = property
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            initial_data["property_sum"] = s1_data["property_sum"]
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            initial_data["interior_decoration"] = bool(s1_data.get("interior_decoration", False))
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            initial_data["interior_decoration_summ"] = s1_data.get("interior_decoration_summ", 0)
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            initial_data["environment"] = bool(s1_data.get("environment", False))
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            initial_data["environment_summ"] = s1_data.get("environment_summ", 0)
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            initial_data["household_effects"] = bool(s1_data.get("household_effects", False))
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            initial_data["household_effects_summ"] = s1_data.get("household_effects_summ", 0)
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
            initial_data["civil_liability"] = bool(s1_data.get("civil_liability", False))
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            initial_data["civil_liability_summ"] = s1_data.get("civil_liability_summ", 0)
        except (ObjectDoesNotExist, KeyError):
            ok = False


    return form_extra_data, initial_data


def _s2_read_data(cd):
    s2_data = {}
    for key in cd:
        if key.startswith("factor_") and cd[key]:
            s2_data[key] = True
    if cd["franchise"] is not None:  # Integer.
        s2_data["franchise"] = cd["franchise"]
    return s2_data


def _s2_read_form_data(s2_data):
    initial_data = {}
    form_extra_data = {}
    if s2_data:
        for key in s2_data:
            if key.startswith("factor_"):
                initial_data[key] = s2_data[key]
        if s2_data.has_key("franchise"):
            initial_data["franchise"] = s2_data["franchise"]

    return form_extra_data, initial_data


socket.setdefaulttimeout(settings.SERVLET_TIMEOUT)


def _build_servlet_request_data(s1_data, s2_data):
    request = {"property": s1_data["property"],
               "property_sum": s1_data["property_sum"],
               "city": s1_data["city"]}

    if s1_data.has_key("interior_decoration"):
        request["interior_decoration"] = u"on"
        request["interior_decoration_summ"] = s1_data["interior_decoration_summ"]

    if s1_data.has_key("environment"):
        request["environment"] = u"on"
        request["environment_summ"] = s1_data["environment_summ"]

    if s1_data.has_key("household_effects"):
        request["household_effects"] = u"on"
        request["household_effects_summ"] = s1_data["household_effects_summ"]

    if s1_data.has_key("civil_liability"):
        request["civil_liability"] = u"on"
        request["civil_liability_summ"] = s1_data["civil_liability_summ"]

    if s2_data:
        for key in s2_data:
            if s2_data[key] == True:
                request[key] = "on"
            else:
                request[key] = s2_data[key]

    return request

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
                                                              company_condition_insurance = 4)
                    if comment:
                        company['company_comment'] = comment[0].company_condition_comment
                    else:
                        company['company_comment'] = ''
                    try:
                        rating = float(company["raiting"])
                        company["rating_stars"] = rating / 2
                    except ValueError:
                        company["rating_stars"] = 0.0
    return result, msg
