# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from profile.models import Persona

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

class InsurancePolicy(models.Model):
    # ==== Business logic-related fields ====
    persona = models.ForeignKey(Persona, verbose_name=u"Персона")
    type = models.SmallIntegerField(verbose_name=u"Тип полиса",
                                    choices=TYPE_CHOICES, default=1)
    payment = models.CharField(verbose_name=u"Оплата", max_length=10,
                               default="unpayed", choices=PAYMENT_CHOICES)
    state = models.CharField(verbose_name=u"Статус полиса", max_length=10,
                             default="init", choices=STATE_CHOICES)
    # ==== Insurance-related fields ====
    buy_date = models.DateField(verbose_name=u"Начала периода страхования")
    end_date = models.DateField(verbose_name=u"Конец периода страхования")
    experience_driving = models.PositiveSmallIntegerField(
        verbose_name=u"Стаж вождения",
        validators=[MinValueValidator(1), MaxValueValidator(60)])
    insurance_years = models.PositiveSmallIntegerField(
        verbose_name=u"Количество лет использования страховки",
        choices=zip(range(1, 9), range(1, 9)))
    insurance_usage = models.PositiveSmallIntegerField(
        verbose_name=u"Страховые случаи", choices=USAGE_CHOICES)
    driver_number = models.PositiveSmallIntegerField(
        verbose_name=u"Число водителей",
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    price = models.PositiveIntegerField(
        verbose_name=u"Стоимость объекта страхования")
    # == Авто ==
    mark_id = models.IntegerField(verbose_name=u"Марка авто")
    model_id = models.IntegerField(verbose_name=u"Модель авто")
    model_year_id = models.IntegerField(verbose_name=u"Год выпуска")
    power_id = models.IntegerField(verbose_name=u"Лошадиные силы")
    # == Адреса ==
    formal_address = models.TextField(verbose_name=u"Адрес прописки")
    real_address = models.TextField(verbose_name=u"Адрес прописки")
    delivery_address = models.TextField(verbose_name=u"Адрес прописки")

    class Meta:
        verbose_name = u"Страховой полис"
        verbose_name_plural = u"Страховые полисы"

    def clean(self):
        if self.buy_date <= self.end_date:
            raise ValidationError('Конец периода страхования должен быть '\
                                  'позже начала')
