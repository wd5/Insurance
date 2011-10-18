# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from newcalc.models import Mark, City, ModelYear, Power, Model, BurglarAlarm
from profile.models import Persona
from polices.models import BODY_TYPE_CHOICES, SEX_CHOICES, InsurancePolicyData
from email_login.forms import PhoneNumberField
from captcha.fields import CaptchaField
from django.forms import ModelForm

AGE_CHOISES = [(i, i) for i in xrange(18, 81)]
AGE_CHOISES.insert(0, ("", "--------"))
EXPERIENCE_CHOISES = [(i, i) for i in xrange(0, 51)]
EXPERIENCE_CHOISES.insert(0, ("", "--------"))
FRANCHISE_CHOICE = (
    (0, 0),
    (3000, 3000),
    (6000, 6000),
    (9000, 9000),
    (15000, 15000),
    (30000, 30000)
    )
attrs_dict = {'class': 'required'}
class Step1Form(forms.Form):
    country = forms.ModelChoiceField(label="Регистрация ТС",
                                     queryset=City.objects.all(),
                                     empty_label="--------")
    city = forms.ModelChoiceField(label="Территория использования ТС",
                                  queryset=City.objects.all(),
                                  empty_label="--------")
    dago = forms.IntegerField(label="ДАГО", min_value=250000, max_value=25000000)
    violations = forms.ChoiceField(label="Грубые нарушения",
                                   choices=(("no", "не было"), ("yes", "были")))
    power = forms.ModelChoiceField(label="Мощность",
                                   queryset=Power.objects.none(),
                                   empty_label="--------")
    age = forms.ChoiceField(label="Возраст", choices=AGE_CHOISES)
    experience_driving = forms.ChoiceField(label="Стаж вождения",
                                           choices=EXPERIENCE_CHOISES)

    def __init__(self, *args, **kwargs):
        form_extra_data = kwargs.pop("form_extra_data")
        super(Step1Form, self).__init__(*args, **kwargs)
        self.fields['power'].queryset = Power.objects.all()

    def clean(self):
        cd = self.cleaned_data
        return cd

    # COMMENT: временное упрощение
    # def clean_price(self):
    #     price = self.cleaned_data['price']
    #     power = self.cleaned_data['power']
    #     price_obj = Price.objects.get(price_power=power)
    #     if not price_obj.price_min < price < price_obj.price_max:
    #         raise forms.ValidationError(
    #             "Стоимость должна быть от %d до %d." % (price_obj.price_min,
    #                                                     price_obj.price_max))
    #     return price

    def clean_experience_driving(self):
        age = int(self.cleaned_data["age"])
        experience_driving = int(self.cleaned_data["experience_driving"])
        if age - experience_driving < 18:
            raise forms.ValidationError("Опыт вождения не может отсчитываться "\
                                        "от возраста, меньшего 18.")
        return self.cleaned_data["experience_driving"]


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
    burglar_alarm_group = forms.ModelChoiceField(label="Сигнализация",
                                                 queryset=BurglarAlarm.objects.filter(
                                                     pk__gt=0,
                                                     burglar_alarm_parent=0).order_by("burglar_alarm_name"),
                                                 empty_label="--------",
                                                 required=False)
    burglar_alarm_model = forms.ModelChoiceField(label="Модель сигнализации",
                                                 queryset=BurglarAlarm.objects.none()
                                                 , empty_label="--------",
                                                 required=False)

    def __init__(self, *args, **kwargs):
        form_extra_data = kwargs.pop("form_extra_data")
        super(Step2Form, self).__init__(*args, **kwargs)
        if form_extra_data.has_key("burglar_alarm_group"):
            self.fields['burglar_alarm_model'].queryset = form_extra_data[
                                                          "burglar_alarm_group"].models.order_by("burglar_alarm_name")

    def clean_burglar_alarm_group(self):
        burglar_alarm_group = self.cleaned_data['burglar_alarm_group']
        if (burglar_alarm_group is not None and
            burglar_alarm_group.models.all().count()):
            self.fields[
            'burglar_alarm_model'].queryset = burglar_alarm_group.models.order_by("burglar_alarm_name")
            self.fields['burglar_alarm_model'].required = True
        return burglar_alarm_group


class Step3FormReg(forms.Form):
    pass


class Step3FormNoReg(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    middle_name = forms.CharField(max_length=30)
    phone = PhoneNumberField()
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label="Email address")
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict),
        label="Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict),
        label="Password (again)")

    #captcha = CaptchaField()

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    "The two password fields didn't match.")
        return self.cleaned_data

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                "This email address is already in use. Please supply a different email address.")
        return self.cleaned_data['email']

    def clean_phone(self):
        if self.cleaned_data['phone'] == "":
            raise forms.ValidationError(
                "Недопустимые символы в номере телефона.")
        return self.cleaned_data['phone']


class Step4Form(ModelForm):
    class Meta:
        model = InsurancePolicyData
        exclude = ('polisy',)
