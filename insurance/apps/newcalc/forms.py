# -*- coding: utf-8 -*-
from django import forms
from models import Mark, City, ModelYear, Power, Model, Mym, Price

AGE_CHOISES = [(i, i) for i in xrange(18, 81)]
AGE_CHOISES.insert(0, ("", "--------"))
EXPERIENCE_CHOISES = [(i, i) for i in xrange(0, 51)]
EXPERIENCE_CHOISES.insert(0, ("", "--------"))

class Step1Form(forms.Form):
    mark = forms.ModelChoiceField(label="Марка автомобиля",
        queryset=Mark.objects.all(), empty_label="--------")
    model = forms.ModelChoiceField(label="Модель автомобиля",
        queryset=Model.objects.none(), empty_label="--------")
    model_year = forms.ModelChoiceField(label="Год выпуска",
        queryset=ModelYear.objects.none(), empty_label="--------")
    power = forms.ModelChoiceField(label="Мощность",
        queryset=Power.objects.none(), empty_label="--------")
    price = forms.IntegerField(label="Стоимость")
    wheel = forms.ChoiceField(label="Руль", choices=((0, "левый"), (1, "правый")))
    city = forms.ModelChoiceField(label="Регистрация собственника",
        queryset=City.objects.all(), empty_label="--------")
    credit = forms.BooleanField(label="Кредит", required=False)
    unlimited_users = forms.BooleanField(label="Неограниченное число " \
                                               "пользователей", required=False)
    age = forms.ChoiceField(label="Возраст", choices=AGE_CHOISES)
    experience_driving = forms.ChoiceField(label="Стаж вождения",
        choices=EXPERIENCE_CHOISES)

    def __init__(self, *args, **kwargs):
        form_extra_data = kwargs.pop("form_extra_data")
        super(Step1Form, self).__init__(*args, **kwargs)
        if form_extra_data.has_key("mark"):
            self.fields['model'].queryset = form_extra_data["mark"].model_set.all()
            if form_extra_data.has_key("model"):
                self.fields['model_year'].queryset = \
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

    def clean_unlimited_users(self):
        unlimited_users = self.cleaned_data['unlimited_users']
        if unlimited_users:
            self.fields['age'].required = False
            self.fields['experience_driving'].required = False
        return unlimited_users
