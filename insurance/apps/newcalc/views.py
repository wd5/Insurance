# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.utils import simplejson
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from models import Mark, Model, Mym, ModelYear, Power, City, Price
from forms import Step1Form


@login_required
def step1(request):
    if request.method == "POST":
        form = Step1Form(request.POST, form_extra_data={})
        if form.is_valid():
            cd = form.cleaned_data
            s1_data = {}
            s1_data["mark"] = cd["mark"].pk
            s1_data["model"] = cd["model"].pk
            s1_data["model_year"] = cd["model_year"].pk
            s1_data["power"] = cd["power"].pk
            s1_data["price"] = cd["price"]
            s1_data["wheel"] = int(cd["wheel"])  # Integer.
            s1_data["city"] = cd["city"].pk
            s1_data["credit"] = cd["credit"]  # Bool.
            s1_data["unlimited_users"] = cd["unlimited_users"]  # Bool.
            s1_data["price"] = cd["price"]
            age = cd.get("age")
            if not age:
                age = None  # Empty string handling.
            else:
                age = int(age)
            s1_data["age"] = age
            experience_driving = cd.get("experience_driving")
            if not experience_driving and experience_driving != 0:
                experience_driving = None  # Empty string handling.
            else:
                experience_driving = int(experience_driving)
            s1_data["experience_driving"] = experience_driving
            request.session["s1_data"] = s1_data
            return HttpResponse("Form is valid.")
    else:
        initial_data = {}
        form_extra_data = {}
        s1_data = request.session.get("s1_data")
        if s1_data:
            try:
                mark = Mark.objects.get(pk=s1_data.get("mark"))
            except ObjectDoesNotExist:
                ok = False
            else:
                initial_data["mark"] = mark
                form_extra_data["mark"] = mark
                ok = True
            if ok:
                try:
                    model = Model.objects.get(pk=s1_data.get("model"))
                except ObjectDoesNotExist:
                    ok = False
                else:
                    initial_data["model"] = model
                    form_extra_data["model"] = model
            if ok:
                try:
                    model_year = ModelYear.objects.get(pk=s1_data.get("model_year"))
                except ObjectDoesNotExist:
                    ok = False
                else:
                    initial_data["model_year"] = model_year
                    form_extra_data["model_year"] = model_year
            if ok:
                try:
                    power = Power.objects.get(pk=s1_data.get("power"))
                except ObjectDoesNotExist:
                    ok = False
                else:
                    initial_data["power"] = power
            if ok:
                try:
                    price = s1_data["price"]
                except KeyError:
                    ok = False
                else:
                    initial_data["price"] = price
            if ok:
                try:
                    wheel = s1_data["wheel"]
                except KeyError:
                    ok = False
                else:
                    initial_data["wheel"] = wheel
            if ok:
                try:
                    city = City.objects.get(pk=s1_data.get("city"))
                except ObjectDoesNotExist:
                    ok = False
                else:
                    initial_data["city"] = city
            if ok:
                try:
                    credit = s1_data["credit"]
                except KeyError:
                    ok = False
                else:
                    initial_data["credit"] = credit
            if ok:
                try:
                    unlimited_users = s1_data["unlimited_users"]
                except KeyError:
                    ok = False
                else:
                    initial_data["unlimited_users"] = unlimited_users
            if ok:
                try:
                    age = s1_data["age"]
                except KeyError:
                    ok = False
                else:
                    if age:
                        initial_data["age"] = age
            if ok:
                try:
                    experience_driving = s1_data["experience_driving"]
                except KeyError:
                    pass
                else:
                    if experience_driving is not None:
                        initial_data["experience_driving"] = experience_driving
        form = Step1Form(form_extra_data=form_extra_data, initial=initial_data)
    return direct_to_template(request, 'calc/step1.html', {"s1_form": form,})


# AJAX.
@login_required
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


@login_required
@require_GET
def get_years(request):
    response_dict = {}
    if request.is_ajax() and request.GET.has_key("model"):
        try:
            model = Model.objects.get(pk=request.GET["model"])
        except ObjectDoesNotExist:
            pass
        else:
            years = model.modelyear_set.all()
            for year in years:
                response_dict[year.year_id] = year.model_year_year
    response = simplejson.dumps(response_dict)
    return HttpResponse(response, mimetype='application/javascript')


@login_required
@require_GET
def get_powers(request):
    response_dict = {}
    if request.is_ajax() and request.GET.has_key("model") and \
       request.GET.has_key("year"):
        try:
            mym = Mym.objects.get(mym_y=request.GET["year"],
                                  mym_m=request.GET["model"])
        except ObjectDoesNotExist:
            pass
        else:
            powers = mym.power_set.all()
            for power in powers:
                response_dict[power.power_id] = power.power_name
    response = simplejson.dumps(response_dict)
    return HttpResponse(response, mimetype='application/javascript')


@login_required
@require_GET
def get_price(request):
    response = ""
    if request.is_ajax() and request.GET.has_key("power"):
        try:
            power = Power.objects.get(pk=request.GET["power"])
        except ObjectDoesNotExist:
            pass
        else:
            try:
                price = Price.objects.get(price_power=power)
            except ObjectDoesNotExist:
                pass
            else:
                response = "от %d до %d" % (price.price_min, price.price_max)
    return HttpResponse(response, mimetype='text/plain')
