# -*- coding: utf-8 -*-
from django import forms
from models import Mark, City, ModelYear, Power, Model, Mym, Price, BurglarAlarm

AGE_CHOISES = [(i, i) for i in xrange(18, 81)]
AGE_CHOISES.insert(0, ("", "--------"))
EXPERIENCE_CHOISES = [(i, i) for i in xrange(0, 51)]
EXPERIENCE_CHOISES.insert(0, ("", "--------"))
FRANCHISE_STEP = 5000

class Step1Form(forms.Form):
    mark = forms.ModelChoiceField(label="Марка автомобиля",
                                  queryset=Mark.objects.all(),
                                  empty_label="--------")
    model = forms.ModelChoiceField(label="Модель автомобиля",
                                   queryset=Model.objects.none(),
                                   empty_label="--------")
    model_year = forms.ModelChoiceField(label="Год выпуска",
                                        queryset=ModelYear.objects.none(),
                                        empty_label="--------")
    power = forms.ModelChoiceField(label="Мощность",
                                   queryset=Power.objects.none(),
                                   empty_label="--------")
    price = forms.IntegerField(label="Стоимость")
    wheel = forms.ChoiceField(label="Руль",
                              choices=(("left", "левый"), ("right", "правый")))
    city = forms.ModelChoiceField(label="Регистрация собственника",
                                  queryset=City.objects.all(),
                                  empty_label="--------")
    credit = forms.BooleanField(label="Кредит", required=False)
    age = forms.ChoiceField(label="Возраст", choices=AGE_CHOISES)
    experience_driving = forms.ChoiceField(label="Стаж вождения",
                                           choices=EXPERIENCE_CHOISES)

    def __init__(self, *args, **kwargs):
        form_extra_data = kwargs.pop("form_extra_data")
        super(Step1Form, self).__init__(*args, **kwargs)
        if form_extra_data.has_key("mark"):
            self.fields['model'].queryset = form_extra_data[
                                            "mark"].model_set.all()
            if form_extra_data.has_key("model"):
                self.fields['model_year'].queryset =\
                form_extra_data["model"].modelyear_set.all()
                if form_extra_data.has_key("model_year"):
                    mym = Mym.objects.get(mym_y=form_extra_data["model_year"],
                                          mym_m=form_extra_data["model"])
                    self.fields['power'].queryset = mym.power_set.all()

    def clean_mark(self):
        mark = self.cleaned_data['mark']
        self.fields['model'].queryset = mark.model_set.all()  # My hack :)
        return mark

    def clean_model(self):
        model = self.cleaned_data['model']
        self.fields['model_year'].queryset = model.modelyear_set.all()
        return model

    def clean_model_year(self):
        model_year = self.cleaned_data['model_year']
        model = self.cleaned_data['model']
        mym = Mym.objects.get(mym_y=model_year, mym_m=model)
        self.fields['power'].queryset = mym.power_set.all()
        return model_year

    def clean_price(self):
        price = self.cleaned_data['price']
        power = self.cleaned_data['power']
        price_obj = Price.objects.get(price_power=power)
        if not price_obj.price_min < price < price_obj.price_max:
            raise forms.ValidationError(
                "Стоимость должна быть от %d до %d." % (price_obj.price_min,
                                                        price_obj.price_max))
        return price


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
    franchise = forms.IntegerField(label="Франшиза", min_value=0,
                                   max_value=20000,
                                   required=False)
    burglar_alarm_group = forms.ModelChoiceField(label="Сигнализация",
             queryset=BurglarAlarm.objects.filter(pk__gt=0, burglar_alarm_parent=0),
             empty_label="--------", required=False)
    burglar_alarm_model = forms.ModelChoiceField(label="Модель сигнализации",
             queryset=BurglarAlarm.objects.none(), empty_label="--------",
             required=False)

    def __init__(self, *args, **kwargs):
        form_extra_data = kwargs.pop("form_extra_data")
        super(Step2Form, self).__init__(*args, **kwargs)
        if form_extra_data.has_key("burglar_alarm_group"):
            self.fields['burglar_alarm_model'].queryset = form_extra_data[
                                            "burglar_alarm_group"].models.all()

    def clean_franchise(self):
        franchise = self.cleaned_data["franchise"]
        if isinstance(franchise, int) and franchise % FRANCHISE_STEP:
            raise forms.ValidationError("Значение должно быть "\
                                        "кратно %d" % FRANCHISE_STEP)
        return franchise

    def clean_burglar_alarm_group(self):
        burglar_alarm_group = self.cleaned_data['burglar_alarm_group']
        if burglar_alarm_group is not None and burglar_alarm_group.models.all().count():
            self.fields['burglar_alarm_model'].queryset = burglar_alarm_group.models.all()
            self.fields['burglar_alarm_model'].required = True
        return burglar_alarm_group

