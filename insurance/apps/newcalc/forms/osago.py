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
    mark = forms.ModelChoiceField(label="Марка автомобиля",
                                  queryset=Mark.objects.all(),
                                  empty_label="Выберите марку автомобиля")
    model = forms.ModelChoiceField(label="Модель автомобиля",
                                   queryset=Model.objects.none(),
                                   empty_label="Выберите модель автомобиля")
    model_year = forms.ModelChoiceField(label="Год выпуска",
                                        queryset=ModelYear.objects.none(),
                                        empty_label="--------")
    city = forms.ModelChoiceField(label="Территория использования ТС",
                                  queryset=City.objects.all(),
                                  empty_label="--------")
    dago = forms.IntegerField(label="Гражданская ответственность", max_value=25000000)
    violations = forms.ChoiceField(label="Грубые нарушения",
                                   choices=(("1", "не было"), ("1.5", "были")))
    power = forms.ModelChoiceField(label="Мощность",
                                   queryset=Power.objects.none(),
                                   empty_label="--------")
    age = forms.ChoiceField(label="Возраст", choices=AGE_CHOISES)
    experience_driving = forms.ChoiceField(label="Стаж вождения",
                                           choices=EXPERIENCE_CHOISES)
    unlimited_drivers = forms.BooleanField(
        label="Неограниченное число водителей",
        required=False)
    age1 = forms.ChoiceField(label="Возраст второго водителя",
                             choices=AGE_CHOISES,
                             required=False)
    experience_driving1 = forms.ChoiceField(
        label="Стаж вождения второго водителя",
        choices=EXPERIENCE_CHOISES,
        required=False)
    age2 = forms.ChoiceField(label="Возраст третьего водителя",
                             choices=AGE_CHOISES, required=False)
    experience_driving2 = forms.ChoiceField(label="Стаж вождения третьего "\
                                                  "водителя",
                                            choices=EXPERIENCE_CHOISES,
                                            required=False)
    age3 = forms.ChoiceField(label="Возраст четвертого водителя",
                             choices=AGE_CHOISES, required=False)
    experience_driving3 = forms.ChoiceField(label="Стаж вождения четвертого "\
                                                  "водителя",
                                            choices=EXPERIENCE_CHOISES,
                                            required=False)

    def __init__(self, *args, **kwargs):
        form_extra_data = kwargs.pop("form_extra_data")
        super(Step1Form, self).__init__(*args, **kwargs)
        if form_extra_data.has_key("mark"):
            self.fields['model'].queryset = form_extra_data[
                                            "mark"].model_set.filter(model_active=1)
            if form_extra_data.has_key("model"):
                # COMMENT: временное упрощение
                # self.fields['model_year'].queryset =\
                # form_extra_data["model"].modelyear_set.all()
                self.fields['model_year'].queryset = ModelYear.objects.all()
                if form_extra_data.has_key("model_year"):
                    # COMMENT: временное упрощение
                    # mym = Mym.objects.get(mym_y=form_extra_data["model_year"],
                    #                       mym_m=form_extra_data["model"])
                    # self.fields['power'].queryset = mym.power_set.all()
                    self.fields['power'].queryset = Power.objects.all()

    def clean_mark(self):
        mark = self.cleaned_data['mark']
        self.fields['model'].queryset = mark.model_set.all()  # My hack :)
        return mark

    def clean_model(self):
        model = self.cleaned_data['model']
        self.fields['model_year'].queryset = ModelYear.objects.all()
        return model

    def clean_model_year(self):
        model_year = self.cleaned_data['model_year']
        # model = self.cleaned_data['model']
        # mym = Mym.objects.get(mym_y=model_year, mym_m=model)
        # self.fields['power'].queryset = mym.power_set.all()
        self.fields['power'].queryset = Power.objects.all()
        return model_year

    def clean(self):
        cd = self.cleaned_data
        unlimited_drivers = cd["unlimited_drivers"]
        age1 = cd.get("age1")
        age2 = cd.get("age2")
        age3 = cd.get("age3")
        experience_driving1 = cd.get("experience_driving1")
        experience_driving2 = cd.get("experience_driving2")
        experience_driving3 = cd.get("experience_driving3")
        if not unlimited_drivers:
            if (age1 and not experience_driving1) or (experience_driving1 and
                                                      not age1):
                raise forms.ValidationError("Не полностью заполнены данные "\
                                            "по второму водителю.")
            if (age2 and not experience_driving2) or (experience_driving2 and
                                                      not age2):
                raise forms.ValidationError("Не полностью заполнены данные по "\
                                            "третьему водителю.")
            if (age3 and not experience_driving3) or (experience_driving3 and
                                                      not age3):
                raise forms.ValidationError("Не полностью заполнены данные по "\
                                            "четвертому водителю.")
                # На случай отключенного js.
            if age2 and not age1:
                raise forms.ValidationError("Нужно заполнить данные по "\
                                            "второму водителю, прежде, чем заполнять по третьему.")
            if age3 and not age2:
                raise forms.ValidationError("Нужно заполнить данные по "\
                                            "третьему водителю, прежде, чем заполнять по четвертому.")
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

    def clean_experience_driving1(self):
        age1 = self.cleaned_data.get("age1")
        experience_driving1 = self.cleaned_data.get("experience_driving1")
        if age1 and experience_driving1:
            if int(age1) - int(experience_driving1) < 18:
                raise forms.ValidationError("Опыт вождения не может "\
                                            "отсчитываться от возраста, меньшего 18.")
        return experience_driving1

    def clean_experience_driving2(self):
        age2 = self.cleaned_data.get("age2")
        experience_driving2 = self.cleaned_data.get("experience_driving2")
        if age2 and experience_driving2:
            if int(age2) - int(experience_driving2) < 18:
                raise forms.ValidationError("Опыт вождения не может "\
                                            "отсчитываться от возраста, меньшего 18.")
        return experience_driving2

    def clean_experience_driving3(self):
        age3 = self.cleaned_data.get("age3")
        experience_driving3 = self.cleaned_data.get("experience_driving3")
        if age3 and experience_driving3:
            if int(age3) - int(experience_driving3) < 18:
                raise forms.ValidationError("Опыт вождения не может "\
                                            "отсчитываться от возраста, меньшего 18.")
        return experience_driving3


class Step2Form(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super(Step2Form, self).__init__(*args, **kwargs)


class Step3FormReg(forms.Form):
    pass


class Step3FormNoReg(forms.Form):
    first_name = forms.CharField(max_length=20)
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

    captcha = CaptchaField()

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


#class Step4Form(ModelForm):
#    class Meta:
#        model = InsurancePolicyData
#        exclude = ('polisy',)

from kasko import Step4Form, Step5Form, Step6Form
