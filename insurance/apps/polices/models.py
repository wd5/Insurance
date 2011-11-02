# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('init', 'Заявка'),
    ('process', 'В оформлении'),
    ('active', 'Действителен'),
    ('ended', 'Срок действия истек'),
    )

STATUS_PAYMENT_CHOICES = (
    ('payed', 'Оплачено'),
    ('unpayed', 'Не оплачено'),
    )

TYPE_CHOICES = (
    (1, u'КАСКО'),
    (2, u'ОСАГО'),
    (3, u'ДМС'),
    (4, u'ОМС'),
    (5, u'Другие'),
    )

USAGE_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4+'),
    )

WHEEL_CHOICES = (
    ("left", "левый"),
    ("right", "правый"),
    )

BODY_TYPE_CHOICES = (
    (u"Седан", u"Седан"),
    (u"Хетчбэк 3дв", u"Хетчбэк 3дв"),
    (u"Хетчбэк 5дв", u"Хетчбэк 5дв"),
    (u"Универсал", u"Универсал"),
    (u"Кабриолет", u"Кабриолет"),
    (u"Пикап", u"Пикап"),
    (u"Фургон", u"Фургон"),
    (u"Купе", u"Купе"),
    (u"Лимузин", u"Лимузин"),
    (u"Внедорожник", u"Внедорожник"),
    (u"Иное", u"Иное"),
)

SEX_CHOICES = (
    (u'м', u"Мужчина"),
    (u'ж', u"Женщина"),
)

CATEGORY_CHOICES = (
    (1, 'B'),
    (2, 'C'),
    (3, 'D'),
    )
CITIZEN_CHOICES = (
    (1, 'Гражданин РФ'),
    (2, 'Иностранный гражданин'),
    )
KPP_CHOICES = (
    (1, 'Механическая'),
    (2, 'Автомат'),
    )
MOTOR_CHOICES = (
    (1, 'Бензиновый'),
    (2, 'Дизельный'),
    (3, 'Гибридный'),
    )
PAYMENT_CHOICES = (
    (1, 'Наличными'),
    (2, 'Картой')
)
TIME_CHOICES = (
    (datetime.time(9, 30), u"9:30 - 12:00"),
    (datetime.time(12, 0), u"12:00 - 15:00"),
    (datetime.time(15, 0), u"15:00 - 18:00")
)

BUILDING_CHOICES = (
    (1, u'Кирпичное'),
    (2, u'Панельное'),
    (3, u'Деревянное')
    )

class CallRequests(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    date = models.DateTimeField(u'Дата заявки', auto_now_add=True)
    phone = models.CharField(u'Телефонный номер', max_length=14)
    comment = models.CharField(u'Комментарий', max_length=255, blank = True, null=True)

    class Meta:
        verbose_name = u'Заказ звонка'
        verbose_name_plural = u'Заказы звонка'

class InsurancePolicy(models.Model):
    user = models.ForeignKey(User)
    type = models.SmallIntegerField("Тип полиса", choices=TYPE_CHOICES,
                                    default=1)
    payment = models.CharField("Оплата", max_length=10, default="unpayed",
                               choices=STATUS_PAYMENT_CHOICES)
    state = models.CharField("Статус полиса", max_length=10, default="init",
                             choices=STATE_CHOICES)
    company = models.CharField("Страховая компания", max_length=100)
    mark = models.CharField("Марка", max_length=20)
    model = models.CharField("Модель", max_length=50)
    model_year = models.PositiveIntegerField("Год выпуска")
    power_str = models.CharField(u'Мощность(строкой)', blank=True, null=True, max_length=20)
    #power = models.PositiveIntegerField("Мощность", blank=True, null=True) #WTF в модели POWER варчар, тут инт? Либо добавить надо в Павер еще одно поле инт с мощностью, либо это сделать варчаром.
    price = models.PositiveIntegerField("Стоимость")
    wheel = models.CharField("Руль", choices=WHEEL_CHOICES, max_length=5)
    city = models.CharField("Нас. пункт", max_length=50)
    credit = models.BooleanField("Кредит")
    unlimited_users = models.BooleanField("Неограниченно число пользователей")
    age = models.PositiveSmallIntegerField("Возраст")
    experience_driving = models.PositiveSmallIntegerField("Опыт вождения")
    age1 = models.PositiveSmallIntegerField("Возраст(2-й водитель)", blank=True,
                                            null=True)
    experience_driving1 = models.PositiveSmallIntegerField("Опыт вождения(2-й "\
                                                           "водитель)",
                                                           blank=True, null=True)
    age2 = models.PositiveSmallIntegerField("Возраст(3-й водитель)", blank=True,
                                            null=True)
    experience_driving2 = models.PositiveSmallIntegerField("Опыт вождения(3-й "\
                                                           "водитель)",
                                                           blank=True, null=True)
    age3 = models.PositiveSmallIntegerField("Возраст(4-й водитель)", blank=True,
                                            null=True)
    experience_driving3 = models.PositiveSmallIntegerField("Опыт вождения(4-й "\
                                                           "водитель)",
                                                           blank=True, null=True)
    # Extra info.
    first_name = models.CharField("Имя страхователя", max_length=30, null=True, blank=True)
    last_name = models.CharField("Фамилия страхователя", max_length=30, null=True, blank=True)
    middle_name = models.CharField("Отчество страхователя", max_length=30, null=True, blank=True)
    birth_date = models.DateField("Дата рождения страхователя", null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES)
    category = models.PositiveIntegerField(u'категория прав', choices=CATEGORY_CHOICES, null=True, blank=True, max_length=1)
    citizenship = models.PositiveIntegerField(u'Гражданство', choices=CITIZEN_CHOICES, null=True, blank=True )
    passport_series = models.CharField(u'Серия паспорта', max_length=30, null=True, blank=True)
    passport_number = models.CharField(u'Номер паспорта', max_length=30,null=True, blank=True)
    issued_org = models.CharField(u'Кем выдан', max_length=255, null=True, blank=True)
    issued_date = models.DateField(u'Дата выдачи', null=True, blank=True)

    reg_region = models.CharField(u'Область, край', max_length=255, null=True, blank=True)
    reg_area = models.CharField(u'Район', max_length=255, null=True, blank=True)
    reg_city = models.CharField(u'Населенный пункт', max_length=255,null=True, blank=True)
    reg_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    reg_index = models.CharField(u'Индекс', max_length=16, null=True, blank=True)
    reg_building = models.CharField(u'Дом', max_length=16, null=True, blank=True)
    reg_housing = models.CharField(u'Корпус', max_length=6, null=True, blank=True)
    reg_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)

    live_region = models.CharField(u'Область, край', max_length=255, null=True, blank=True)
    live_area = models.CharField(u'Район', max_length=255, null=True, blank=True)
    live_city = models.CharField(u'Населенный пункт', max_length=255,null=True, blank=True)
    live_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    live_index = models.CharField(u'Индекс', max_length=16, null=True, blank=True)
    live_building = models.CharField(u'Дом', max_length=16, null=True, blank=True)
    live_housing = models.CharField(u'Корпус', max_length=6, null=True, blank=True)
    live_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)
#STEP 4-2
    vin = models.CharField("VIN", max_length=17, null=True, blank=True)
    number = models.CharField("Гос. номер", null=True, blank=True, max_length=10)
    body_number = models.CharField("Номер кузова", null=True, blank=True, max_length=17)
    body_type = models.CharField("Тип кузова", max_length=15, choices=BODY_TYPE_CHOICES, null=True, blank=True)

    pts_number = models.CharField(u"Серия и номер ПТС", max_length=10, null=True, blank=True)
    pts_date = models.DateField(u"Дата выдачи ПТС", null=True, blank=True)
    power = models.PositiveIntegerField(u"Мощность", null=True, blank=True)
    volume = models.PositiveIntegerField(u"Объем двигателя", null=True, blank=True)
    mileage = models.IntegerField(u"Пробег", null=True, blank=True)
    kpp = models.PositiveSmallIntegerField(u"Коробка передач", choices=KPP_CHOICES, max_length=1, default=1, null=True, blank=True)
    motor = models.PositiveSmallIntegerField(u"Двигатель", choices=MOTOR_CHOICES, max_length=1, default=1, null=True, blank=True)

    owner_last_name = models.CharField("Фамилия", max_length=30, null=True, blank=True)
    owner_first_name = models.CharField("Имя", max_length=30, null=True, blank=True)
    owner_middle_name = models.CharField("Отчество", max_length=30, null=True, blank=True)
    owner_birth_date = models.DateField("Дата рождения", null=True, blank=True)
    first_owner = models.BooleanField("Первый владелец авто", default=True)
    owner_sex = models.CharField("Пол владельца", max_length=1, choices=SEX_CHOICES)
#STEP 4-3
    date = models.DateField("Дата доставки", null=True, blank=True)
    time = models.TimeField("Время доставки", null=True, blank=True, choices=TIME_CHOICES)
    street = models.CharField(u'Улица доставки', max_length=255, null=True, blank=True)
    building = models.CharField(u'Дом доставки', max_length=16, null=True, blank=True)
    structure = models.CharField(u'Строение доставки', max_length=16, null=True, blank=True)
    housing = models.CharField(u'Корпус доставки', max_length=6, null=True, blank=True)
    floor = models.CharField(u'Этаж доставки', max_length=6, null=True, blank=True)
    domophone = models.CharField(u'Код домофона', max_length=12, null=True, blank=True)
    flat = models.CharField(u'Квартира доставки', max_length=6, null=True, blank=True)
    porch = models.CharField(u'Подъезд доставки', max_length=6, null=True, blank=True)
    payments = models.PositiveSmallIntegerField(u'Вариант оплаты', null=True,
                                blank=True, choices=PAYMENT_CHOICES, default=1)
    comment = models.TextField(u'Комментарий', null=True, blank=True)

    class Meta:
        verbose_name = "Страховой полис"
        verbose_name_plural = "Страховые полисы"

#    def clean(self):
#        if self.buy_date <= self.end_date:
#            raise ValidationError('Конец периода страхования должен быть '\
#                                  'позже начала')
#
class InsurancePolicyData(models.Model):
    # TODO: To remove!
    polisy = models.ForeignKey('InsurancePolicy', null=True, blank=True)
    first_name = models.CharField("Имя страхователя", max_length=30, null=True, blank=True)
    last_name = models.CharField("Фамилия страхователя", max_length=30, null=True, blank=True)
    middle_name = models.CharField("Отчество страхователя", max_length=30, null=True, blank=True)
    birth_date = models.DateField("Дата рождения страхователя", null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES)
    category = models.PositiveIntegerField(u'категория прав', choices=CATEGORY_CHOICES, null=True, blank=True, max_length=1)
    citizenship = models.PositiveIntegerField(u'Гражданство', choices=CITIZEN_CHOICES, null=True, blank=True )
    passport_series = models.CharField(u'Серия паспорта', max_length=30, null=True, blank=True)
    passport_number = models.CharField(u'Номер паспорта', max_length=30,null=True, blank=True)
    issued_org = models.CharField(u'Кем выдан', max_length=255, null=True, blank=True)
    issued_date = models.DateField(u'Дата выдачи', null=True, blank=True)

    reg_region = models.CharField(u'Область, край', max_length=255, null=True, blank=True)
    reg_area = models.CharField(u'Район', max_length=255, null=True, blank=True)
    reg_city = models.CharField(u'Населенный пункт', max_length=255,null=True, blank=True)
    reg_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    reg_index = models.CharField(u'Индекс', max_length=16, null=True, blank=True)
    reg_building = models.CharField(u'Дом', max_length=16, null=True, blank=True)
    reg_housing = models.CharField(u'Корпус', max_length=6, null=True, blank=True)
    reg_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)

    live_region = models.CharField(u'Область, край', max_length=255, null=True, blank=True)
    live_area = models.CharField(u'Район', max_length=255, null=True, blank=True)
    live_city = models.CharField(u'Населенный пункт', max_length=255,null=True, blank=True)
    live_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    live_index = models.CharField(u'Индекс', max_length=16, null=True, blank=True)
    live_building = models.CharField(u'Дом', max_length=16, null=True, blank=True)
    live_housing = models.CharField(u'Корпус', max_length=6, null=True, blank=True)
    live_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)
#STEP 4-2
    vin = models.CharField("VIN", max_length=17, null=True, blank=True)
    number = models.CharField("Гос. номер", null=True, blank=True, max_length=10)
    body_number = models.CharField("Номер кузова", null=True, blank=True, max_length=10)
    body_type = models.CharField("Тип кузова", max_length=15, choices=BODY_TYPE_CHOICES, null=True, blank=True)

    pts_number = models.CharField(u"Серия и номер ПТС", max_length=10, null=True, blank=True)
    pts_date = models.DateField(u"Дата выдачи ПТС", null=True, blank=True)
    power = models.PositiveIntegerField(u"Мощность", null=True, blank=True)
    volume = models.PositiveIntegerField(u"Объем двигателя", null=True, blank=True)
    mileage = models.IntegerField(u"Пробег", null=True, blank=True)
    kpp = models.PositiveSmallIntegerField(u"Коробка передач", choices=KPP_CHOICES, max_length=1, default=1, null=True, blank=True)
    motor = models.PositiveSmallIntegerField(u"Двигатель", choices=MOTOR_CHOICES, max_length=1, default=1, null=True, blank=True)

    owner_last_name = models.CharField("Фамилия", max_length=30, null=True, blank=True)
    owner_first_name = models.CharField("Имя", max_length=30, null=True, blank=True)
    owner_middle_name = models.CharField("Отчество", max_length=30, null=True, blank=True)
    owner_birth_date = models.DateField("Дата рождения", null=True, blank=True)
    first_owner = models.BooleanField("Первый владелец авто", default=True)
    owner_sex = models.CharField("Пол владельца", max_length=1, choices=SEX_CHOICES)
#STEP 4-3
    date = models.DateField("Дата доставки", null=True, blank=True)
    time = models.TimeField("Время доставки", null=True, blank=True, choices=TIME_CHOICES)
    street = models.CharField(u'Улица доставки', max_length=255, null=True, blank=True)
    building = models.CharField(u'Дом доставки', max_length=16, null=True, blank=True)
    structure = models.CharField(u'Строение доставки', max_length=16, null=True, blank=True)
    housing = models.CharField(u'Корпус доставки', max_length=6, null=True, blank=True)
    floor = models.CharField(u'Этаж доставки', max_length=6, null=True, blank=True)
    domophone = models.CharField(u'Этаж доставки', max_length=6, null=True, blank=True)
    flat = models.CharField(u'Квартира доставки', max_length=6, null=True, blank=True)
    porch = models.CharField(u'Квартира доставки', max_length=6, null=True, blank=True)
    payments = models.PositiveSmallIntegerField(u'вариант оплаты', null=True, blank=True, choices=PAYMENT_CHOICES, default=1)
    comment = models.TextField(u'Комментарий', null=True, blank=True)

class InsurancePolicyIFL(models.Model):
    user = models.ForeignKey(User)
    type = models.SmallIntegerField("Тип полиса", choices=TYPE_CHOICES,
                                    default=6)
    payment = models.CharField("Оплата", max_length=10, default="unpayed",
                               choices=STATUS_PAYMENT_CHOICES)
    state = models.CharField("Статус полиса", max_length=10, default="init",
                             choices=STATE_CHOICES)
    company = models.CharField("Страховая компания", max_length=100)

    city = models.CharField("Нас. пункт", max_length=50)
    property = models.CharField("Имущество", max_length=30)
    property_sum = models.PositiveIntegerField("Стоимость имущества")

    interior_decoration = models.PositiveIntegerField("Стоимость отделки")
    environment = models.PositiveIntegerField("Стоимость оборудования")
    household_effects = models.PositiveIntegerField("Стоимость домашнего имущества")
    civil_liability = models.PositiveIntegerField("Сумма гражданской ответственности")

    # extra data
    first_name = models.CharField("Имя страхователя", max_length=30, null=True, blank=True)
    last_name = models.CharField("Фамилия страхователя", max_length=30, null=True, blank=True)
    middle_name = models.CharField("Отчество страхователя", max_length=30, null=True, blank=True)
    birth_date = models.DateField("Дата рождения страхователя", null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES)
    citizenship = models.PositiveIntegerField(u'Гражданство', choices=CITIZEN_CHOICES, null=True, blank=True )
    passport_series = models.CharField(u'Серия паспорта', max_length=30, null=True, blank=True)
    passport_number = models.CharField(u'Номер паспорта', max_length=30,null=True, blank=True)
    issued_org = models.CharField(u'Кем выдан', max_length=255, null=True, blank=True)
    issued_date = models.DateField(u'Дата выдачи', null=True, blank=True)

    reg_region = models.CharField(u'Область, край', max_length=255, null=True, blank=True)
    reg_area = models.CharField(u'Район', max_length=255, null=True, blank=True)
    reg_city = models.CharField(u'Населенный пункт', max_length=255,null=True, blank=True)
    reg_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    reg_index = models.CharField(u'Индекс', max_length=16, null=True, blank=True)
    reg_building = models.CharField(u'Дом', max_length=16, null=True, blank=True)
    reg_housing = models.CharField(u'Корпус', max_length=6, null=True, blank=True)
    reg_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)

    live_region = models.CharField(u'Область, край', max_length=255, null=True, blank=True)
    live_area = models.CharField(u'Район', max_length=255, null=True, blank=True)
    live_city = models.CharField(u'Населенный пункт', max_length=255,null=True, blank=True)
    live_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    live_index = models.CharField(u'Индекс', max_length=16, null=True, blank=True)
    live_building = models.CharField(u'Дом', max_length=16, null=True, blank=True)
    live_housing = models.CharField(u'Корпус', max_length=6, null=True, blank=True)
    live_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)

# STEP4-2 IFL
    object_city = models.CharField(u'Населенный пункт', max_length=255, null=True, blank=True)
    object_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    object_index = models.CharField(u'Индекс', max_length=6, null=True, blank=True)
    object_building = models.CharField(u'Дом', max_length=4, null=True, blank=True)
    object_housing = models.CharField(u'Корпус', max_length=4, null=True, blank=True)
    object_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)
    object_built_year = models.PositiveIntegerField(u"Год постройки", null=True, blank=True)
    object_overhaul_year = models.PositiveIntegerField(u"Год капитального ремонта", null=True, blank=True)
    object_size = models.CharField(u'Общая площадь квартиры (кв. м.)', max_length=4, null=True, blank=True)
    object_floor = models.CharField(u'Этаж', max_length=2, null=True, blank=True)

    policy_start = models.DateField("Дата начала действия полиса", null=True, blank=True)
    building_type = models.PositiveSmallIntegerField(u"Тип здания", choices=BUILDING_CHOICES, null=True, blank=True)

    last_repair = models.PositiveIntegerField(u"Год проведения последней внутренней отделки",
                                              null=True, blank=True)

#STEP 4-3
    date = models.DateField("Дата доставки", null=True, blank=True)
    time = models.TimeField("Время доставки", null=True, blank=True, choices=TIME_CHOICES)
    street = models.CharField(u'Улица доставки', max_length=255, null=True, blank=True)
    building = models.CharField(u'Дом доставки', max_length=16, null=True, blank=True)
    structure = models.CharField(u'Строение доставки', max_length=16, null=True, blank=True)
    housing = models.CharField(u'Корпус доставки', max_length=6, null=True, blank=True)
    floor = models.CharField(u'Этаж доставки', max_length=6, null=True, blank=True)
    domophone = models.CharField(u'Код домофона', max_length=12, null=True, blank=True)
    flat = models.CharField(u'Квартира доставки', max_length=6, null=True, blank=True)
    porch = models.CharField(u'Подъезд доставки', max_length=6, null=True, blank=True)
    payments = models.PositiveSmallIntegerField(u'Вариант оплаты', null=True,
                                blank=True, choices=PAYMENT_CHOICES, default=1)
    comment = models.TextField(u'Комментарий', null=True, blank=True)


class InsurancePolicyForeign(models.Model):
    user = models.ForeignKey(User)
    type = models.SmallIntegerField("Тип полиса", choices=TYPE_CHOICES,
                                    default=5)
    payment = models.CharField("Оплата", max_length=10, default="unpayed",
                               choices=STATUS_PAYMENT_CHOICES)
    state = models.CharField("Статус полиса", max_length=10, default="init",
                             choices=STATE_CHOICES)
    company = models.CharField("Страховая компания", max_length=100)

    age = models.PositiveSmallIntegerField("Возраст страхователя")
    trip_type = models.CharField("Тип поездки", max_length=30)
    insurance_summ = models.PositiveIntegerField("Сумма страхования")
    countries = models.CharField("Страны действия", max_length=30)
    territory = models.CharField("Территория действия", max_length=30)
    trip_purpose = models.CharField("Цель поездки", max_length=30)

    # extra data
    first_name = models.CharField("Имя страхователя", max_length=30, null=True, blank=True)
    last_name = models.CharField("Фамилия страхователя", max_length=30, null=True, blank=True)
    middle_name = models.CharField("Отчество страхователя", max_length=30, null=True, blank=True)
    birth_date = models.DateField("Дата рождения страхователя", null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES)
    citizenship = models.PositiveIntegerField(u'Гражданство', choices=CITIZEN_CHOICES, null=True, blank=True )
    passport_series = models.CharField(u'Серия паспорта', max_length=30, null=True, blank=True)
    passport_number = models.CharField(u'Номер паспорта', max_length=30,null=True, blank=True)
    issued_org = models.CharField(u'Кем выдан', max_length=255, null=True, blank=True)
    issued_date = models.DateField(u'Дата выдачи', null=True, blank=True)

    reg_region = models.CharField(u'Область, край', max_length=255, null=True, blank=True)
    reg_area = models.CharField(u'Район', max_length=255, null=True, blank=True)
    reg_city = models.CharField(u'Населенный пункт', max_length=255,null=True, blank=True)
    reg_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    reg_index = models.CharField(u'Индекс', max_length=16, null=True, blank=True)
    reg_building = models.CharField(u'Дом', max_length=16, null=True, blank=True)
    reg_housing = models.CharField(u'Корпус', max_length=6, null=True, blank=True)
    reg_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)

    live_region = models.CharField(u'Область, край', max_length=255, null=True, blank=True)
    live_area = models.CharField(u'Район', max_length=255, null=True, blank=True)
    live_city = models.CharField(u'Населенный пункт', max_length=255,null=True, blank=True)
    live_street = models.CharField(u'Улица', max_length=255, null=True, blank=True)
    live_index = models.CharField(u'Индекс', max_length=16, null=True, blank=True)
    live_building = models.CharField(u'Дом', max_length=16, null=True, blank=True)
    live_housing = models.CharField(u'Корпус', max_length=6, null=True, blank=True)
    live_flat = models.CharField(u'Квартира', max_length=6, null=True, blank=True)





#STEP 4-3
    date = models.DateField("Дата доставки", null=True, blank=True)
    time = models.TimeField("Время доставки", null=True, blank=True, choices=TIME_CHOICES)
    street = models.CharField(u'Улица доставки', max_length=255, null=True, blank=True)
    building = models.CharField(u'Дом доставки', max_length=16, null=True, blank=True)
    structure = models.CharField(u'Строение доставки', max_length=16, null=True, blank=True)
    housing = models.CharField(u'Корпус доставки', max_length=6, null=True, blank=True)
    floor = models.CharField(u'Этаж доставки', max_length=6, null=True, blank=True)
    domophone = models.CharField(u'Код домофона', max_length=12, null=True, blank=True)
    flat = models.CharField(u'Квартира доставки', max_length=6, null=True, blank=True)
    porch = models.CharField(u'Подъезд доставки', max_length=6, null=True, blank=True)
    payments = models.PositiveSmallIntegerField(u'Вариант оплаты', null=True,
                                blank=True, choices=PAYMENT_CHOICES, default=1)
    comment = models.TextField(u'Комментарий', null=True, blank=True)
