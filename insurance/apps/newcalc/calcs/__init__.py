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
