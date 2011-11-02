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

from newcalc.models import TripType, TripPurpose, Company, CompanyCondition, InsuranceType, \
    KackoParameters, TripCountries, TripTerritory
from newcalc.forms.foreign import Step1Form, Step2Form, Step3FormReg, Step3FormNoReg
from newcalc.forms.foreign import Step4Form, Step5Form, Step6Form
from polices.forms import CallRequestForm
from profile.models import Persona
from polices.models import InsurancePolicyForeign #, CallRequests
from email_login.backends import RegistrationBackend
from newcalc.servlet import servlet_request
from newcalc.templatetags.intspace import intspace

# ========== General views ==========

def success(request):
    request.session['policy_foreign'] = None
    return direct_to_template(request, 'calc/success.html', {'tab': 5})


S1_REQUIRED_KEYS = (
    "trip_type", "insurance_summ", "trip_purpose", "countries", "age", "territory")


def step1(request, prev=0):
    if prev != 0:
        prev_int = int(prev)
        pr_data =  request.session.get("s1_data_foreign%d" % prev_int)
        curr_data =  request.session.get("s1_data_foreign")
        if pr_data is None:
            raise Http404
        if prev_int == 1:
            request.session["s1_data_foreign1"] = curr_data
            request.session["s1_data_foreign"] = pr_data
        else:  # 2.
            k1 =  request.session.get("s1_data_foreign1")
            request.session["s1_data_foreign2"] = k1
            request.session["s1_data_foreign1"] = curr_data
            request.session["s1_data_foreign"] = pr_data
        return redirect(reverse('ncalc_step1_foreign'))
    if request.method == "POST":
        form = Step1Form(request.POST)
        if form.is_valid():
            new_data = _s1_read_data(form.cleaned_data)
            k1 =  request.session.get("s1_data_foreign1")
            k0 =  request.session.get("s1_data_foreign")
            # Избегаем дублирования.
            if k0 and not (new_data["trip_type"]==k0["trip_type"] and
                           new_data["countries"]==k0["countries"] and
                           new_data["insurance_summ"]==k0["insurance_summ"]
                           and new_data["trip_purpose"]==k0["trip_purpose"]):
                if k1:
                    request.session["s1_data_foreign2"] = k1
                request.session["s1_data_foreign1"] = k0
            request.session["s1_data_foreign"] = new_data
            return redirect(reverse('ncalc_step2_foreign'))
    else:
        initial_data = {}
        form_extra_data = {}
        s1_data = request.session.get("s1_data_foreign")
        if s1_data:
            form_extra_data, initial_data = _s1_read_form_data(s1_data)
        else:
            initial_data['insurance_summ'] = 0
            initial_data["territory"] = 1
        form = Step1Form(initial=initial_data)
    k1 =  request.session.get("s1_data_foreign1")
    k2 =  request.session.get("s1_data_foreign2")
    prev_data = []
    if k1:
        ttype = TripType.objects.get(pk=k1["trip_type"]).trip_type_name
        countries = TripCountries.objects.get(pk=k1["countries"]).vzr_countries_name
        price = k1["insurance_summ"]
        purp = TripPurpose.objects.get(pk=k1["trip_purpose"]).trip_purpose_name
        prev_data.append(u"%s / %s / %s / $%s" % (ttype, countries, purp, intspace(price)))
    if k2:
        ttype = TripType.objects.get(pk=k2["trip_type"]).trip_type_name
        countries = TripCountries.objects.get(pk=k2["countries"]).vzr_countries_name
        price = k2["insurance_summ"]
        purp = TripPurpose.objects.get(pk=k2["trip_purpose"]).trip_purpose_name
        prev_data.append(u"%s / %s / %s / $%s" % (ttype, countries, purp, intspace(price)))

    return direct_to_template(request, 'calc/foreign/step1.html', {"s1_form": form,
                                                                   "prev_data": prev_data, 'tab': 5})


def step2(request):
    """
    TODO:
    - валидация данных s1_data из сессии?
    """
    s1_data = request.session.get("s1_data_foreign")
    s2_data = request.session.get("s2_data_foreign")

    if not s1_data:
        return redirect(reverse('ncalc_step1_foreign'))
    for k in S1_REQUIRED_KEYS:
        if not s1_data.has_key(k):
            return redirect(reverse('ncalc_step1_foreign'))
    if not s2_data:
        s2_data = dict()
        s2_data['factor_price'] = True #Если нет данных => только перешли ко 2 шагу - сортируем по цене
    result = servlet_request(_build_servlet_request_data(s1_data, s2_data), servlet_type="foreign")
    if result is None:
        err_text = "Превышен лимит ожидания. Не получен ответ сервлета в "\
                   "течение %d сек." % settings.SERVLET_TIMEOUT
        return direct_to_template(request, "calc/error.html", {"err_text": err_text, 'tab': 5})

    result, msg = _parse_servlet_response(result)

    data = {}
    data["trip_type"] = TripType.objects.get(pk=s1_data["trip_type"]).trip_type_name
    # small hack for better display
    if data["trip_type"] == u"Краткосрочная":
        data["trip_type"] = u"Краткосрочная поездка"
    data["countries"] = TripCountries.objects.get(pk=s1_data["countries"]).vzr_countries_name
    data["price"] = s1_data["insurance_summ"]

    if request.method == "POST":
        form = Step2Form(request.POST)
        if form.is_valid():
            request.session["s2_data_foreign"] = _s2_read_data(form.cleaned_data)
            return redirect(reverse('ncalc_step2_foreign'))
    else:
        form_extra_data, initial_data = _s2_read_form_data(s2_data)
        form = Step2Form(initial=initial_data)
    table = KackoParameters.objects.filter(is_active=True)
    header = dict()
    for t in table:
        header[t.kparameter_alias] = {'name':t.kparameter_name, 'comment':t.kparameter_comment}
    return direct_to_template(request, 'calc/foreign/step2.html', {"msg": msg, 'tab': 5,
                                                                   "s1_form": form,
                                                                   "result": result,
                                                                   "header":header,
                                                                   "data": data})


def step3(request, alias):
    call_form = CallRequestForm()
    s1_data = request.session.get("s1_data_foreign")
    if not s1_data:
        return redirect(reverse('ncalc_step1_foreign'))
    data = {}
    data["alias"] = alias
    data["insurance_type"] = "ВЗР"

    data["trip_type"] = TripType.objects.get(pk=s1_data["trip_type"]).trip_type_name
    data["trip_purpose"] = TripPurpose.objects.get(pk=s1_data["trip_purpose"]).trip_purpose_name
    data["territory"] = TripTerritory.objects.get(pk=s1_data["territory"]).vzr_territory_name
    data["countries"] = TripCountries.objects.get(pk=s1_data["countries"]).vzr_countries_name
    data["insurance_summ"] = s1_data["insurance_summ"]
    data["age"] = s1_data["age"]

    data["company"] = Company.objects.get(company_alias=alias).company_name

    data["registered"] = request.session.has_key("new_user")

    if request.method == "POST":
        if request.user.is_authenticated() or request.session.has_key("new_user"):
            form = Step3FormReg(request.POST)
            if form.is_valid():

                if request.session.has_key("new_user"):
                    user = User.objects.get(pk=request.session["new_user"])
                else:
                    user = request.user

                request.session["company_alias"] = alias
                ip = InsurancePolicyForeign()
                ip.user = user
                ip.company = Company.objects.get(company_alias=alias).company_full_name
                ip.trip_type = TripType.objects.get(pk=s1_data["trip_type"]).trip_type_name
                ip.trip_purpose = TripPurpose.objects.get(pk=s1_data["trip_purpose"]).trip_purpose_name
                ip.insurance_summ = s1_data["insurance_summ"]
                ip.territory = TripTerritory.objects.get(pk=s1_data["territory"]).vzr_territory_name
                ip.countries = TripCountries.objects.get(pk=s1_data["countries"]).vzr_countries_name
                ip.age = s1_data["age"]
                policy = ip.save()
                request.session['policy_foreign'] = ip.pk

                return redirect(reverse('ncalc_step4_foreign'))
        else:
            form = Step3FormNoReg(request.POST)
            if form.is_valid():
                new_user = RegistrationBackend().register(request,
                                                          **form.cleaned_data)
                request.session["new_user"] = new_user.pk
                return redirect(reverse('ncalc_step3_foreign', args=[alias, ]))
    else:
        if request.user.is_authenticated():
            form = Step3FormReg()
        else:
            form = Step3FormNoReg()
    if request.user.is_authenticated():
        return direct_to_template(request, 'calc/foreign/step3reg.html', {"data": data, "form": form, "call_form":call_form, 'tab': 5})
    else:
        return direct_to_template(request, 'calc/foreign/step3noreg.html', {"data": data, "form": form, "call_form":call_form, 'tab': 5})

def step4(request):
    policy_id = request.session.get('policy_foreign')
    if not policy_id:
        return redirect(reverse('ncalc_step1_foreign')) #, args=[request.session.get('company_alias')]))
    policy = InsurancePolicyForeign.objects.get(pk=policy_id)
    policy_data = InsurancePolicyForeign.objects.values().get(pk=policy_id)
    if request.method == 'POST':
        form = Step4Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for k in cd.keys():
                if cd[k]:
                    setattr(policy, k, cd[k])
            policy.save()
            return redirect(reverse('ncalc_step5_foreign'))
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
    return direct_to_template(request, 'calc/foreign/step4.html', {"form": form, 'tab': 5})


def step5(request):
    policy_id = request.session.get('policy_foreign')
    if not policy_id:
        return redirect(reverse('ncalc_step1_foreign')) #, args=[request.session.get('company_alias')]))
    policy = InsurancePolicyForeign.objects.get(pk=policy_id)
    policy_data = InsurancePolicyForeign.objects.values().get(pk=policy_id)

    if request.method == 'POST':
        form = Step5Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for k in cd.keys():
                if cd[k]:
                    setattr(policy, k, cd[k])
            policy.save()
            return redirect(reverse('ncalc_step6_foreign'))
    else:
        form = Step5Form(initial=policy_data)

    copy = {"first_name": policy.first_name,
            "middle_name": policy.middle_name,
            "last_name": policy.last_name,
            "birth_date": policy.birth_date.strftime("%d.%m.%Y"),
            "sex": policy.sex}
    return direct_to_template(request, 'calc/foreign/step5.html', {"form": form, "tab": 5,
                                                                   "copy": copy,
                                                                   "back": reverse("ncalc_step4_foreign")})

def step6(request):
    policy_id = request.session.get('policy_foreign')
    if not policy_id:
        return redirect(reverse('ncalc_step1_foreign')) #, args=[request.session.get('company_alias')]))
    policy = InsurancePolicyForeign.objects.get(pk=policy_id)
    policy_data = InsurancePolicyForeign.objects.values().get(pk=policy_id)

    if request.method == 'POST':
        form = Step6Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for k in cd.keys():
                if cd[k]:
                    setattr(policy, k, cd[k])
            policy.save()
            return redirect(reverse('ncalc_success_foreign'))
    else:
        form = Step6Form(initial=policy_data)
    return direct_to_template(request, 'calc/foreign/step6.html', {"form": form, 'tab': 5,
                                                                   "back": reverse("ncalc_step5_foreign")})

# ========== Auxilary ==========


def _s1_read_data(cd):
    s1_data = {}
    s1_data["trip_type"] = cd["trip_type"].pk
    s1_data["trip_purpose"] = cd["trip_purpose"].pk
    s1_data["age"] = cd["age"]
    s1_data["insurance_summ"] = cd["insurance_summ"]
    s1_data["countries"] = cd["countries"].pk
    s1_data["territory"] = cd["territory"].pk
    return s1_data


def _s1_read_form_data(s1_data):
    initial_data = {}
    form_extra_data = {}
    ok = True

    if ok:
        try:
            trip_type = TripType.objects.get(pk=s1_data.get("trip_type"))
            initial_data["trip_type"] = trip_type
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            trip_purpose = TripPurpose.objects.get(pk=s1_data.get("trip_purpose"))
            initial_data["trip_purpose"] = trip_purpose
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            summ = s1_data.get("insurance_summ", 0)
            initial_data["insurance_summ"] = summ
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            countries = TripCountries.objects.get(pk=s1_data.get("countries"))
            initial_data["countries"] = countries
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            territory = TripCountries.objects.get(pk=s1_data.get("territory"))
            initial_data["territory"] = territory
        except (ObjectDoesNotExist, KeyError):
            ok = False

    if ok:
        try:
            age = s1_data["age"]
            initial_data["age"] = age
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

    servlet_request_data = {"type_trip": s1_data["trip_type"],
                            "countries": s1_data["countries"],
                            "insurance_summ": s1_data["insurance_summ"],
                            "target_trip": s1_data["trip_purpose"],
                            "territory": s1_data["territory"],
                            "age": s1_data["age"]}
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
                    comment = CompanyCondition.objects.filter(company_condition_company = company_id)[:1]
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
