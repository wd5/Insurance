# -*- coding: utf-8 -*-
import json
import sys,urllib,urllib2

from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to

from calc.forms import ServletTestForm, CalcStepOneForm, CalcStepTwoForm
from calc.utils_db import connect,get_mark_by_id,get_model_by_id
from calc.utils_db import get_mark_model_year_json
from calc.utils_db import get_power_by_id,get_model_year_by_id,get_city_by_id

import settings

def calc_step_1(request):
    # Структура:
    # 0) Подготовительные операции
    # 1) Первый вход (GET) Никаких параметров нет
    # 2) Вход по кнопке формы (POST)
    # 3) Вход по нажатию кнопки назад из второго шага калькулятора
    # ---------- 0) ----------
    # Получаем данные из базы (упакованные в json)
    # Потом передадим их в переменные js
    marks,models,years = get_mark_model_year_json()
    extra_content = {'marks':marks,
                     'models':models,
                     'years':years,}
    if(request.POST):
        extra_content['request_type'] = "'POST'"
    else:
        extra_content['request_type'] = "'GET'"
    # ---------- 1) ----------
    if request.META["REQUEST_METHOD"] == "GET" and request.GET == {}:
        extra_content['calc_step_one_form'] = CalcStepOneForm()
        return direct_to_template(request, 'calc_step_1.html',extra_content)
    # ---------- 2) ----------
    if(request.POST):
       calc_step_one_form = CalcStepOneForm(request.POST)
       if calc_step_one_form.is_valid():
           # Переходим к calc_step_2
           # Создать строку параметров GET
           url = "/calc/calc_step_2/?"
           for k,v in calc_step_one_form.cleaned_data.items():
               url += "%s=%s&" % (k,v)
           url = url.rstrip('&')
           return(redirect_to(request,url=url))
       else:
           extra_content['calc_step_one_form'] = calc_step_one_form
           if request.POST.__contains__('mark'):
               if request.POST['mark'] == '1000':
                   extra_content['mark_error'] = 'Вы не выбрали марку автомобиля'
               else:
                   extra_content['mark'] = request.POST['mark']
           return direct_to_template(request, 'calc_step_1.html',extra_content)
    # ---------- 3) ----------
    # Если есть параметр GET в запросе, считать параметры и передать
    # в темплату для установки начальных значений в форме
    js_str = ''
    # if request.GET.has_key('mark'):
    if request.META["REQUEST_METHOD"] == "GET" and request.GET != {}:
        js_str += '{'
        for k,v in request.GET.items():
            js_str += '"%s":"%s",' % (k,v)
        js_str = js_str.rstrip(',')
        js_str += '}'
        extra_content['js_str'] = js_str
        extra_content['calc_step_one_form'] = CalcStepOneForm()
        return direct_to_template(request, 'calc_step_1.html',extra_content)

def calc_step_2(request):
    # Если нет запроса GET, перенаправляем на первый шаг
    if not request.GET.has_key('mark'):
        return(redirect_to(request,url='/calc/calc_step_1'))

    # Получить параметры GET для запроса
    servlet_request_data = {}
    for k,v in request.GET.items():
        if v == True:
            servlet_request_data[k] = 'on'
        elif v == False:
            servlet_request_data[k] = ''
        else:
            servlet_request_data[k] = v

    calc_step_two_form = CalcStepTwoForm(request.POST or None)
    if calc_step_two_form.is_valid():
        # Добавить параметры формы в данные для запроса к сервлету
        for k,v in calc_step_two_form.cleaned_data.items():
            if v == True:
                servlet_request_data[k] = 'on'
            elif v == False:
                servlet_request_data[k] = ''
            else:
                servlet_request_data[k] = v
        
        # extra_content = {}
        # return redirect('/calc/calc_step_3', extra_content)
       

    # Получить результаты расчета от сервлета
    url = settings.SERVLET_URL
    form_data = urllib.urlencode(servlet_request_data)
    req = urllib2.Request(url, form_data)
    response = urllib2.urlopen(req)
    result_json = response.read()
    result = json.loads(result_json)

    extra_content = {}
    extra_content["result"] = result
    # Для ссылки "Назад"
    extra_content["query_str"] = request.META['QUERY_STRING']
    # Обработка параметров GET, получаем нужные данные, вставляем их в
    # контекст для показа на странице. Часть данных получим из базы
    # insservlet (названия по id)
    extra_content["calc_step_two_form"] = calc_step_two_form
    # Передача параметров из первого шага через GET
    db = connect()
    extra_content["mark"] = get_mark_by_id(db,request.GET["mark"])
    extra_content["model"] = get_model_by_id(db,request.GET["model"])
    extra_content["model_year"] = get_model_year_by_id(db,request.GET["model_year"])
    if request.GET["weel"] == "left":
        extra_content["weel"] = u"Левый"
    else:
        extra_content["weel"] = u"Правый"
    extra_content["power"] = get_power_by_id(db,request.GET["power"])
    extra_content["city"] = get_city_by_id(db,request.GET["city"])
    extra_content["price"] = request.GET["price"]
    if request.GET.has_key("credit"):
        extra_content["credit"] = u"Да"
    else:
        extra_content["credit"] = u"Нет"
    extra_content["age"] = request.GET["age"]
    extra_content["experience_driving"] = request.GET["experience_driving"]


    return direct_to_template(request, 'calc_step_2.html',extra_content)


def calc_step_3(request):
    
    extra_content = {}
    return direct_to_template(request,'calc_step_3.html',extra_content)

