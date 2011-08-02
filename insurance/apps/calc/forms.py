# -*- coding: utf-8 -*-
from django import forms
from calc.utils_db import connect
from calc.utils_db import get_choices

class ServletTestForm(forms.Form):
    """
    """

    def __init__(self,*args,**kwargs):
        super(ServletTestForm,self).__init__(*args,**kwargs)
        db = connect()
        insurance_type_choices = get_choices(db,
                                             id_field='insurance_type_id',
                                             name_field='insurance_type_name',
                                             table='insurance_type')
        self.fields['insurance_type'] = forms.ChoiceField(choices=insurance_type_choices,
                                                          label='Вид страхования',
                                                          help_text='')

        mark_choices = get_choices(db,
                                  id_field='mark_id',
                                  name_field='mark_name',
                                  table='mark')
        self.fields['mark'] = forms.ChoiceField(choices=mark_choices,
                                                label='Марка автомобиля',
                                                help_text='')
        model_choices = get_choices(db,
                                  id_field='model_id',
                                  name_field='model_name',
                                  table='model')
        self.fields['model'] = forms.ChoiceField(choices=model_choices,
                                                label='Модель автомобиля',
                                                help_text='')
        model_year_choices = get_choices(db,
                                  id_field='model_year_id',
                                  name_field='model_year_year',
                                  table='model_year')
        self.fields['model_year'] = forms.ChoiceField(choices=model_year_choices,
                                                      label='Год выпуска',
                                                      help_text='',
                                                      required=False)
        weel_choices = [('left','Левый'),('right','Правый')]
        self.fields['weel'] = forms.ChoiceField(choices=weel_choices,
                                                      label='Руль',
                                                      help_text='',
                                                      required=False)
        power_choices = get_choices(db,
                                  id_field='power_id',
                                  name_field='power_name',
                                  table='power')
        self.fields['power'] = forms.ChoiceField(choices=power_choices,
                                                 label='Мощность',
                                                 help_text='',
                                                 required=False)

        city_choices = get_choices(db,
                                  id_field='city_id',
                                  name_field='city_name',
                                  table='city')
        self.fields['city'] = forms.ChoiceField(choices=city_choices,
                                                 label='Регистрация собственника',
                                                 help_text='',
                                                 required=False)

    price = forms.CharField(required=False,
                      label='Стоимость, тест: 828000<P<883000',
                      help_text='')

    credit = forms.BooleanField(required=False,
                                label='Кредит',
                                help_text='')

    age = forms.CharField(required=False,
                    label='Возраст',
                    help_text='')


    experience_driving = forms.CharField(required=False,
                           label='Стаж вождения',
                           help_text='')

    factor_price = forms.BooleanField(required=False,
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

class CalcStepOneForm(forms.Form):

    def __init__(self,*args,**kwargs):
        super(CalcStepOneForm,self).__init__(*args,**kwargs)
        db = connect()

        mark_choices = get_choices(db,
                                  id_field='mark_id',
                                  name_field='mark_name',
                                  table='mark')
        self.fields['mark'] = forms.ChoiceField(choices=mark_choices,
                                                label='Марка автомобиля',
                                                help_text='')
        model_choices = get_choices(db,
                                  id_field='model_id',
                                  name_field='model_name',
                                  table='model')
        self.fields['model'] = forms.ChoiceField(choices=model_choices,
                                                label='Модель автомобиля',
                                                help_text='')
        model_year_choices = get_choices(db,
                                  id_field='model_year_id',
                                  name_field='model_year_year',
                                  table='model_year')
        self.fields['model_year'] = forms.ChoiceField(choices=model_year_choices,
                                                      label='Год выпуска',
                                                      help_text='',
                                                      required=False)
        weel_choices = [('left','Левый'),('right','Правый')]
        self.fields['weel'] = forms.ChoiceField(choices=weel_choices,
                                                      label='Руль',
                                                      help_text='',
                                                      required=False)
        power_choices = get_choices(db,
                                  id_field='power_id',
                                  name_field='power_name',
                                  table='power')
        self.fields['power'] = forms.ChoiceField(choices=power_choices,
                                                 label='Мощность',
                                                 help_text='',
                                                 required=False)

        city_choices = get_choices(db,
                                  id_field='city_id',
                                  name_field='city_name',
                                  table='city')
        self.fields['city'] = forms.ChoiceField(choices=city_choices,
                                                 label='Регистрация собственника',
                                                 help_text='',
                                                 required=False)

        age_choices = []
        for a in range(18,100):
            age_choices.append((a,a))
        self.fields['age']  = forms.ChoiceField(choices=age_choices,
                                                label='Стаж вождения',
                                                help_text='')

        experience_choices = []
        for a in range(0,50):
            experience_choices.append((a,a))
        self.fields['experience_driving']  = forms.ChoiceField(choices=experience_choices,
                                                label='',
                                                help_text='')


    price = forms.CharField(required=False,
                      label='Стоимость, тест: 828000<P<883000',
                      help_text='')

    credit = forms.BooleanField(required=False,
                                label='Кредит',
                                help_text='')

    # factor_price = forms.BooleanField(required=False,
    #                                     label='Цена',
    #                                     help_text='')

    # factor_easepay = forms.BooleanField(required=False,
    #                                     label='Простота выплат',
    #                                     help_text='')

    # factor_insuranceterms = forms.BooleanField(required=False,
    #                                            label='Условия страхования',
    #                                            help_text='')

    # factor_qualitysupport = forms.BooleanField(required=False,
    #                                            label='Качество информационной поддержки',
    #                                            help_text='')

    # factor_reputation = forms.BooleanField(required=False,
    #                                        label='Репутация компании',
    #                                        help_text='')

    # factor_accessibility = forms.BooleanField(required=False,
    #                                           label='Доступность компании',
    #                                           help_text='')

    # factor_service = forms.BooleanField(required=False,
    #                                     label='Сервис',
    #                                     help_text='')

class CalcStepTwoForm(forms.Form):

    # def __init__(self,*args,**kwargs):
    #     super(CalcStepOneForm,self).__init__(*args,**kwargs)
    #     db = connect()

    factor_price = forms.BooleanField(required=False,
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
