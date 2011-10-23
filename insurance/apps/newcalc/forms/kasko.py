# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from newcalc.models import Mark, City, ModelYear, Power, Model, BurglarAlarm
from profile.models import Persona
from polices.models import SEX_CHOICES, CATEGORY_CHOICES, CITIZEN_CHOICES
from polices.models import BODY_TYPE_CHOICES, KPP_CHOICES, MOTOR_CHOICES
from polices.models import SEX_CHOICES, TIME_CHOICES, PAYMENT_CHOICES
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
    power = forms.ModelChoiceField(label="Мощность",
                                   queryset=Power.objects.none(),
                                   empty_label="--------")
    price = forms.IntegerField(label="Стоимость", max_value=10000000)
    wheel = forms.ChoiceField(label="Руль",
                              choices=(("left", "левый"), ("right", "правый")))
    city = forms.ModelChoiceField(label="Регистрация собственника",
                                  queryset=City.objects.all(),
                                  empty_label="--------")
    credit = forms.BooleanField(label="Кредит", required=False)
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


#class Step4Form_old(ModelForm):
#    class Meta:
#        model = InsurancePolicyData
#        exclude = ('polisy',)

class Step4Form(forms.Form):
    first_name = forms.CharField(label="Имя страхователя", min_length=2, max_length=20)
    last_name = forms.CharField(label="Фамилия страхователя", min_length=2, max_length=30)
    middle_name = forms.CharField(label="Отчество страхователя", min_length=2, max_length=30)
    birth_date = forms.DateField(label="Дата рождения страхователя")
    sex = forms.ChoiceField(label="Пол", choices=SEX_CHOICES)
    category = forms.ChoiceField(label="Категория прав", choices=CATEGORY_CHOICES)
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
    vin = forms.CharField(label="VIN", min_length=17, max_length=17)
    number = forms.CharField(label="Гос. номер", min_length=8, max_length=9)
    body_number = forms.CharField(label="Номер кузова", min_length=17, max_length=17)
    body_type = forms.ChoiceField(label="Тип кузова", choices=BODY_TYPE_CHOICES)
    pts_number = forms.CharField(label="Серия и номер ПТС", max_length=10)
    pts_date = forms.DateField(label="Дата выдачи ПТС")
    power = forms.IntegerField(label="Мощность", min_value=10, max_value=600)
    volume = forms.IntegerField(label="Объем двигателя", min_value=50, max_value=9999)
    mileage = forms.IntegerField(label="Пробег", min_value=10)
    kpp = forms.ChoiceField(label="Коробка передач", choices=KPP_CHOICES)
    motor = forms.ChoiceField(label="Двигатель", choices=MOTOR_CHOICES)
    owner_last_name = forms.CharField(label="Фамилия", min_length=2, max_length=30)
    owner_first_name = forms.CharField(label="Имя", min_length=2, max_length=20)
    owner_middle_name = forms.CharField(label="Отчество", min_length=2, max_length=30)
    owner_birth_date = forms.DateField(label="Дата рождения")
    first_owner = forms.BooleanField(label="Первый владелец авто", required=False)
    owner_sex = forms.ChoiceField(label="Пол владельца", choices=SEX_CHOICES)


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
