# -*- coding: utf-8 -*-
from django import forms
from calc.utils_db import connect
from calc.utils_db import get_choices

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
        wheel_choices = [('left','Левый'),('right','Правый')]
        self.fields['wheel'] = forms.ChoiceField(choices=wheel_choices,
                                                      label='Руль',
                                                      help_text='',
                                                      required=False)

        self.fields['power'] = forms.IntegerField(label='Мощность',
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

class CalcStepTwoForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(CalcStepTwoForm,self).__init__(*args,**kwargs)

        self.fields['standart_deductible'] = forms.CharField(required=False,
                                                             label='',
                                                             help_text='',)

        self.fields['second_deductible'] = forms.CharField(required=False,
                                                             label='',
                                                             help_text='',)

        civil_liability_choices = []
        for a in range(0,2500000,300000):
            civil_liability_choices.append((a,a))
            self.fields['civil_liability'] = forms.ChoiceField(choices=civil_liability_choices,
                                                                   required=False,
                                                                   label='Гражданскую ответственность (дополнительно к полису ОСАГО) ',)
   

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

    damage_full_destruction = forms.BooleanField(required=False,
                                                 label='Возмещать ущерб только при полной гибели или угоне автомобиля')
    
    not_assure_theft = forms.BooleanField(required=False,
				    label='Не страховать автомобиль от угона',)

    burglar_alarm_choices = ((1,'Тип 1'),
                             (2,'Тип 2'))
    burglar_alarm = forms.ChoiceField(choices=burglar_alarm_choices,
                                   label='Охранная система автомобиля ',)

    single_payment_of_the_policy = forms.BooleanField(required=False,
                                                      label='Единовременная оплата полиса',)

    repair_direction_company = forms.BooleanField(required=False,
                                                  label='Ремонт по направлению страховой компании',)

    repair_official_dealer = forms.BooleanField(required=False,
                                                  label='Ремонт у официального дилера по направлению страховой компании',)

    repair_engineering_centre = forms.BooleanField(required=False,
                                                  label='Ремонт в техническом центре по вашему выбору',)

    payment_on_accounting = forms.BooleanField(required=False,
                                                  label='Выплата деньгами по калькуляции',)

    payment_on_accounting_deterioration = forms.BooleanField(required=False,
                                                  label='Выплата деньгами по калькуляции с учетом износа запасных частей',)

    payment_on_accounting_deterioration = forms.BooleanField(required=False,
                                                  label='Выплата деньгами по калькуляции с учетом износа запасных частей',)

    glass_elements_one_year = forms.BooleanField(required=False,
                                                  label='Стекла и стеклянные элементы. Один раз в год',)

    glass_elements_without_restriction = forms.BooleanField(required=False,
                                                            label='Стекла и стеклянные элементы. Без ограничения',)
    
    repair_3_one_year = forms.BooleanField(required=False,
                                                  label='Ремонт в пределах 3%. Один раз в год',)

    repair_5_two_year = forms.BooleanField(required=False,
                                                  label='Ремонт в пределах 5%. Два раза в год',)

    evacuation = forms.BooleanField(required=False,
                                    label='Эвакуация автомобиля к месту стоянки или ремонта',)

    technical_assistance = forms.BooleanField(required=False,
                                              label='Техническая попощь',)

    call_taxi = forms.BooleanField(required=False,
                                   label='Вызов такси',)

    lease_car = forms.BooleanField(required=False,
                                   label='Аренда автомобиля',)

    departure_two_player_dtp = forms.BooleanField(required=False,
                                                  label='Выезд только на ДТП с двумя и более участниками. Сбор справок',)

    departure_all_dtp = forms.BooleanField(required=False,
                                           label='Выезд на любые ДТП. Сбор справок',)

    health_driver_and_passenger = forms.BooleanField(required=False,
                                                     label='Здоровье водителя и пассажиров',)

    kasko_plus_osago = forms.BooleanField(required=False,
                                          label='Купить полис КАСКО вместе с ОСАГО',)



class CalcStepThreeUserForm(forms.Form):
    
    def __init__(self,*args,**kwargs):
        par_name = 'persona_choices'
        if kwargs.has_key(par_name):
            persona_choices = kwargs['persona_choices']
            par_name = kwargs.pop(par_name)
        super(CalcStepThreeUserForm,self).__init__(*args,**kwargs)
        self.fields['persona'] = forms.ChoiceField(initial=par_name,
                                                   choices=persona_choices,
                                                   required=False,
                                                   label='Владелец полиса')

    formal_address = forms.CharField(required=False,
                                     label='Адрес прописки',
                                     help_text='',
                                     max_length=200)
    real_address = forms.CharField(required=False,
                                   label='Адрес проживания',
                                   help_text='',
                                   max_length=200)
    delivery_address = forms.CharField(required=False,
                                       label='Адрес доставки',
                                       help_text='',
                                       max_length=200)

class CalcStepThreeAnonymForm(forms.Form):
    
    last_name = forms.CharField(required=True,
                                label='Фамилия',
                                help_text='',
                                max_length=64)
    first_name = forms.CharField(required=True,
                                 label='Имя',
                                 help_text='',
				 max_length=64)
    middle_name = forms.CharField(required=True,
                                  label='Отчество',
                                  help_text='',
                                  max_length=64)
    email = forms.EmailField (required=True,
                              label='Адрес электронной почты',
                              help_text='')
    formal_address = forms.CharField(required=False,
                                     label='Адрес прописки',
                                     help_text='',
                                     max_length=200)
    real_address = forms.CharField(required=False,
                                   label='Адрес проживания',
                                   help_text='',
                                   max_length=200)
    delivery_address = forms.CharField(required=False,
                                       label='Адрес доставки',
                                       help_text='',
                                       max_length=200)

