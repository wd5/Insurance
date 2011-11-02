# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from newcalc.models import TripType, TripPurpose, TripTerritory, TripCountries
from profile.models import Persona
from polices.models import SEX_CHOICES, CATEGORY_CHOICES, CITIZEN_CHOICES
from polices.models import BODY_TYPE_CHOICES, KPP_CHOICES, MOTOR_CHOICES
from polices.models import SEX_CHOICES, TIME_CHOICES, PAYMENT_CHOICES
from email_login.forms import PhoneNumberField
from captcha.fields import CaptchaField
from django.forms import ModelForm

FRANCHISE_CHOICE = (
    (0, 0),
    (3000, 3000),
    (6000, 6000),
    (9000, 9000),
    (15000, 15000),
    (30000, 30000)
    )

AGE_CHOISES = [(i, i) for i in xrange(18, 81)]
AGE_CHOISES.insert(0, ("", "--------"))

COUNTRIES_CHOICE = (
    (u"1", u"страны Шенгенского соглашения"),
    (u"2", u"остальные страны")
    )

attrs_dict = {'class': 'required'}
class Step1Form(forms.Form):
    trip_type = forms.ModelChoiceField(label="Тип поездки",
                                  queryset=TripType.objects.all(),
                                  empty_label="--------")
    territory = forms.ModelChoiceField(label="Территория действия договора страхования",
                                  queryset=TripTerritory.objects.all(),
                                  empty_label="--------")
    insurance_summ = forms.IntegerField(label="Сумма страхования", max_value=13000000)
    countries = forms.ModelChoiceField(label="Страны действия договора страхования",
                                  queryset=TripCountries.objects.all(),
                                  empty_label="--------")
    trip_purpose = forms.ModelChoiceField(label="Цель поездки",
                                  queryset=TripPurpose.objects.all(),
                                  empty_label="--------")
    age = forms.ChoiceField(label="Возраст страхователя", choices=AGE_CHOISES)


    def __init__(self, *args, **kwargs):
        super(Step1Form, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data

        return cd


class Step2Form(forms.Form):
    factor_price = forms.BooleanField(label="Сортировка по цене",
                                        required=False)
    factor_easepay = forms.BooleanField(label="Сортировка по простоте выплаты",
                                        required=False)
    factor_insuranceterms = forms.BooleanField(label="Сортировка по условиям "\
                                                     "страхования",
                                               required=False)
    factor_qualitysupport = forms.BooleanField(label="Сортировка по качеству "\
                                                     "информ. поддержки",
                                               required=False)
    factor_reputation = forms.BooleanField(label="Сортировка по популярности "\
                                                 "компании", required=False)
    factor_accessibility = forms.BooleanField(label="Сортировка по удобству "\
                                                    "расположения",
                                              required=False)
    factor_service = forms.BooleanField(label="Сортировка по быстроте покупки",
                                        required=False)
    franchise = forms.ChoiceField(label="Франшиза",
                                  choices=FRANCHISE_CHOICE,
                                  required=False)


    def __init__(self, *args, **kwargs):
        super(Step2Form, self).__init__(*args, **kwargs)


class Step3FormReg(forms.Form):
    pass

from newcalc.forms.kasko import Step3FormNoReg

class Step4Form(forms.Form):
    first_name = forms.CharField(label="Имя страхователя", min_length=2, max_length=20)
    last_name = forms.CharField(label="Фамилия страхователя", min_length=2, max_length=30)
    middle_name = forms.CharField(label="Отчество страхователя", min_length=2, max_length=30)
    birth_date = forms.DateField(label="Дата рождения страхователя")
    sex = forms.ChoiceField(label="Пол", choices=SEX_CHOICES)
    citizenship = forms.ChoiceField(label="Гражданство", choices=CITIZEN_CHOICES)
    passport_series = forms.CharField(label="Серия паспорта", min_length=4, max_length=4)
    passport_number = forms.CharField(label="Номер паспорта", min_length=6, max_length=6)
    issued_org = forms.CharField(label="Кем выдан", min_length=6, max_length=255)
    issued_date = forms.DateField(label="Дата выдачи")
    reg_region = forms.CharField(label="Область, край", min_length=3, max_length=255)
    reg_area = forms.CharField(label="Район", max_length=255, required=False)
    reg_city = forms.CharField(label="Населенный пункт", min_length=2, max_length=255)
    reg_street = forms.CharField(label="Улица", min_length=2, max_length=255)
    reg_index = forms.CharField(label="Индекс", min_length=6, max_length=6)
    reg_building = forms.CharField(label="Дом", max_length=4)
    reg_housing = forms.CharField(label="Корпус", max_length=6, required=False)
    reg_flat = forms.CharField(label="Квартира", max_length=4)
    live_region = forms.CharField(label="Область, край", min_length=3, max_length=255)
    live_area = forms.CharField(label="Район", max_length=255, required=False)
    live_city = forms.CharField(label="Населенный пункт", min_length=2, max_length=255)
    live_street = forms.CharField(label="Улица", min_length=2, max_length=255)
    live_index = forms.CharField(label="Индекс", min_length=6, max_length=6)
    live_building = forms.CharField(label="Дом", max_length=4)
    live_housing = forms.CharField(label="Корпус", max_length=6, required=False)
    live_flat = forms.CharField(label="Квартира", max_length=4)


class Step5Form(forms.Form):
    pass


class Step6Form(forms.Form):
    date = forms.DateField(label="Дата доставки")
    time = forms.ChoiceField(label="Время доставки", choices=TIME_CHOICES)
    street = forms.CharField(label="Улица доставки", min_length=2, max_length=255)
    building = forms.CharField(label="Дом доставки", max_length=4)
    structure = forms.CharField(label="Строение доставки", max_length=4,
                                required=False)
    housing = forms.CharField(label="Корпус доставки", max_length=6, required=False)
    floor = forms.CharField(label="Этаж доставки", max_length=3, required=False)
    domophone = forms.CharField(label="Код домофона", max_length=12, required=False)
    flat = forms.CharField(label="Квартира доставки", max_length=4, required=False)
    porch = forms.CharField(label="Подъезд доставки", max_length=3, required=False)
    payments = forms.ChoiceField(label="Вариант оплаты", choices=PAYMENT_CHOICES)
    comment = forms.CharField(label="Комментарий", required=False,
                              widget=forms.Textarea)
