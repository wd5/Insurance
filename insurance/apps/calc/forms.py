# -*- coding: utf-8 -*-
from django import forms

class ServletTestForm(forms.Form):
    """
    """
    
    insurance_type = forms.CharField(required=False,
                               label='Вид страхования',
                               help_text='')

    mark = forms.CharField(required=False,
                     label='Марка автомобиля',
                     help_text='')

    model = forms.CharField(required=False,
                      label='Модель автомобиля',
                      help_text='')

    model_year = forms.CharField(required=False,
                           label='Год выпуска',
                           help_text='')

    wheel = forms.CharField(required=False,
                      label='Руль',
                      help_text='')

    power = forms.CharField(required=False,
                      label='Мощность',
                      help_text='')

    price = forms.BooleanField(required=False,
                      label='Стоимость',
                      help_text='')

    credit = forms.CharField(required=False,
                       label='Кредит',
                       help_text='')

    city = forms.CharField(required=False,
                     label='Регистрация собственника',
                     help_text='')

    age = forms.CharField(required=False,
                    label='Возраст',
                    help_text='')

    experience = forms.CharField(required=False,
                           label='Стаж вождения',
                           help_text='')

    factor_price = forms.CharField(required=False,
                             label='Цена',
                             help_text='')


    factor_easepay = forms.BooleanField(required=False,
                                        label='Простота выплат',
                                        help_text='')

    factor_insuranceterms = forms.BooleanField(required=False,
                                               label='Условия страхования',
                                               help_text='')

    factor_qualitysupport = forms.BooleanField(required=False,
                                               label='Качество информационной поддержки',
                                               help_text='')
    
    factor_reputation = forms.BooleanField(required=False,
                                           label='Репутация компании',
                                           help_text='')

    factor_accessibility = forms.BooleanField(required=False,
                                              label='Доступность компании',
                                              help_text='')

    factor_service = forms.BooleanField(required=False,
                                        label='Сервис',
                                        help_text='')

