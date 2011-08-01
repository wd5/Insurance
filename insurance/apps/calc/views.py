# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
from calc.forms import ServletTestForm,CalcStepOneForm
import sys,urllib,urllib2
import json
from calc.utils_db import get_mark_model_year_json
from calc.utils_db import connect,get_mark_by_id,get_model_by_id,get_model_year_by_id,get_city_by_id

def servlet_test(request):
    result = ''
    servlet_test_form = ServletTestForm(request.POST or None)
    form_fields = {}
    if servlet_test_form.is_valid():
        for k,v in servlet_test_form.cleaned_data.items():
            print >> sys.stderr, k, "=> ", v
            if v == True:
                form_fields[k] = 'on'
            elif v == False:
                form_fields[k] = ''
            else:
                form_fields[k] = v

        print >> sys.stderr, "----------------------------------------"
        for k,v in form_fields.items():
            strpr = "%-28s%s" % (k,v)
            print >> sys.stderr, strpr
            #print >> sys.stderr, "key =", k, "\tval = ", v
        print >> sys.stderr, "----------------------------------------"

        url = 'http://localhost:8080/ServerIF/MatrixIF'
        #form_fields = servlet_test_form.cleaned_data
        form_data = urllib.urlencode(form_fields)
        req = urllib2.Request(url, form_data)
        response = urllib2.urlopen(req)
        result = response.read()
        # print >> sys.stderr, "result =", result
    extra_content = {'servlet_test_form':servlet_test_form,
                     'result':result}
    return direct_to_template(request, 'servlet_test.html',extra_content)

def calc_step_1(request):
    # Получаем данные из базы (упакованные в json)
    # Потом передадим их в переменные js
    marks,models,years = get_mark_model_year_json()
    calc_step_one_form = CalcStepOneForm(request.POST or None)
    #form_fields = {}
    if calc_step_one_form.is_valid():
        # Переходим к шагу 2
        # Создать строку параметров GET
        url = "/calc/calc_step_2/?"
        for k,v in calc_step_one_form.cleaned_data.items():
            url += "%s=%s&" % (k,v)
        url = url.rstrip('&')
        return(redirect_to(request,url=url))
    # Data for JS
    extra_content = {'marks':marks,'models':models,'years':years}
    # Form
    extra_content['calc_step_one_form'] = calc_step_one_form
    return direct_to_template(request, 'calc_step_1.html',extra_content)

def calc_step_2(request):
    # Если нет запроса GET, перенаправляем на первый шаг
    if not request.GET.has_key('mark'):
        return(redirect_to(request,url='/calc/calc_step_1'))

    # Получить параметры GET для запроса
    form_fields = {}
    for k,v in request.GET.items():
        if v == True:
            form_fields[k] = 'on'
        elif v == False:
            form_fields[k] = ''
        else:
            form_fields[k] = v
    # Получить результаты расчета от сервлета
    url = 'http://localhost:8080/ServerIF/MatrixIF'
    form_data = urllib.urlencode(form_fields)
    req = urllib2.Request(url, form_data)
    response = urllib2.urlopen(req)
    result_json = response.read()
    result = json.loads(result_json)

    extra_content = {}
    extra_content["result"] = result
    extra_content["query_str"] = request.META['QUERY_STRING']
    # Обработка параметров GET, получаем нужные данные, вставляем их в
    # контекст для показа на странице. Часть данных получим из базы
    # insservlet (названия по id)
    db = connect()
    extra_content["mark"] = get_mark_by_id(db,request.GET["mark"])
    extra_content["model"] = get_model_by_id(db,request.GET["model"])
    extra_content["model_year"] = get_model_year_by_id(db,request.GET["model_year"])
    if request.GET["weel"] == "left":
        extra_content["weel"] = u"Левый"
    else:
        extra_content["weel"] = u"Правый"
    extra_content["power"] = request.GET["power"]
    extra_content["city"] = get_city_by_id(db,request.GET["city"])
    extra_content["price"] = request.GET["price"]
    if request.GET.has_key("credit"):
        extra_content["credit"] = u"Да"
    else:
        extra_content["credit"] = u"Нет"
    extra_content["age"] = request.GET["age"]
    extra_content["experience_driving"] = request.GET["experience_driving"]


    return direct_to_template(request, 'calc_step_2.html',extra_content)
