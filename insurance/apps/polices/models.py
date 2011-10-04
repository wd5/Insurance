# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('init', 'Initializing'),
    ('process', 'Being worked on'),
    ('active', 'Active'),
    ('ended', 'Ended'),
    )

PAYMENT_CHOICES = (
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
    ("Седан", "Седан"),
    ("Хетчбэк 3дв", "Хетчбэк 3дв"),
    ("Хетчбэк 5дв", "Хетчбэк 5дв"),
    ("Универсал", "Универсал"),
    ("Кабриолет", "Кабриолет"),
    ("Пикап", "Пикап"),
    ("Фургон", "Фургон"),
    ("Купе", "Купе"),
    ("Лимузин", "Лимузин"),
    ("Внедорожник", "Внедорожник"),
    ("Иное", "Иное"),
)

SEX_CHOICES = (
    ("м", "Мужчина"),
    ("ж", "Женщина"),
)

class InsurancePolicy(models.Model):
    user = models.ForeignKey(User)
    type = models.SmallIntegerField("Тип полиса", choices=TYPE_CHOICES,
                                    default=1)
    payment = models.CharField("Оплата", max_length=10, default="unpayed",
                               choices=PAYMENT_CHOICES)
    state = models.CharField("Статус полиса", max_length=10, default="init",
                             choices=STATE_CHOICES)
    company = models.CharField("Страховая компания", max_length=100)
    mark = models.CharField("Марка", max_length=20)
    model = models.CharField("Модель", max_length=50)
    model_year = models.PositiveIntegerField("Год выпуска")
    power = models.PositiveIntegerField("Мощность", blank=True, null=True)
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
    vin = models.CharField("VIN", max_length=17)
    body_type = models.CharField("Тип кузова", max_length=15,
                                 choices=BODY_TYPE_CHOICES)
    mileage = models.PositiveIntegerField("Пробег")
    last_name = models.CharField("Фамилия", max_length=30)
    first_name = models.CharField("Имя", max_length=30)
    middle_name = models.CharField("Отчество", max_length=30)
    birth_date = models.DateField("Дата рождения")
    first_owner = models.BooleanField("Первый владелец авто")
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES)
    reg_address = models.CharField("Адрес прописки", max_length=200)
    liv_address = models.TextField("Адрес пропроживания", max_length=200)
    pol_address = models.TextField("Адрес доставки полиса", max_length=200)

    class Meta:
        verbose_name = "Страховой полис"
        verbose_name_plural = "Страховые полисы"

#    def clean(self):
#        if self.buy_date <= self.end_date:
#            raise ValidationError('Конец периода страхования должен быть '\
#                                  'позже начала')
