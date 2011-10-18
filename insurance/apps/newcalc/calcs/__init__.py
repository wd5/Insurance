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

from newcalc.models import Company, CompanyCondition
from email_login.backends import RegistrationBackend
from newcalc.servlet import servlet_request



# ========== General views ==========

socket.setdefaulttimeout(settings.SERVLET_TIMEOUT)

def _build_servlet_request_data(s1_data, s2_data):
    if s1_data["credit"]:
        credit_str = "on"
    else:
        credit_str = ""
    unlimited_drivers = s1_data.get("unlimited_drivers")
    if unlimited_drivers is None:
        unlimited_drivers = 0

#TODO: insurance_type!!!

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
                            "unlimited_drivers": unlimited_drivers,
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
                    comment = CompanyCondition.objects.filter(company_condition_company = company_id)[:1]
                    if comment:
                        company['company_comment'] = comment[0].company_condition_comment
                    else:
                        company['company_comment'] = ''
    return result, msg
