# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

from profile.models import Persona



class InsurancePolicy(models.Model):
    # ==== Business logic-related fields ====
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
    
    persona = models.ForeignKey(Persona, verbose_name=u"Персона", null=False, blank=False)
    type = models.SmallIntegerField(verbose_name=u"Тип полиса", null=False, blank=False,
                               choices=TYPE_CHOICES, default=1)
    payment = models.CharField(verbose_name=u"Оплата", max_length=10, null=False, blank=False, default="unpayed",
                               choices=PAYMENT_CHOICES)
    state = models.CharField(verbose_name=u"Статус полиса", max_length=10, null=False, blank=False, default="init",
                             choices=STATE_CHOICES)

    # ==== Insurance-related fields ====
    USAGE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4+'),
    )
    buy_date = models.DateField(verbose_name=u"Начала периода страхования", null=False, blank=False)
    end_date = models.DateField(verbose_name=u"Конец периода страхования", null=False, blank=False)
    experience_driving = models.PositiveSmallIntegerField(verbose_name=u"Стаж вождения",
                                                          null=False, blank=False,
                                                          validators=[MinValueValidator(1), MaxValueValidator(60)])
    insurance_years = models.PositiveSmallIntegerField(verbose_name=u"Количество лет использования страховки",
                                                  null=False, blank=False, choices=zip(range(1,9), range(1,9)))
    insurance_usage = models.PositiveSmallIntegerField(verbose_name=u"Страховые случаи",
                                                  null=False, blank=False, choices=USAGE_CHOICES)
    driver_number = models.PositiveSmallIntegerField(verbose_name=u"Число водителей",
                                                     null=False, blank=False,
                                                     validators=[MinValueValidator(1), MaxValueValidator(10)])
    price = models.PositiveIntegerField(verbose_name=u"Стоимость объекта страхования",
                                        null=False, blank=False)
    # == Авто ==
    mark_id = models.IntegerField(verbose_name=u"Марка авто",
                                  null=False, blank=False)
    model_id = models.IntegerField(verbose_name=u"Модель авто",
                                   null=False, blank=False)
    model_year_id = models.IntegerField(verbose_name=u"Год выпуска",
                                   null=False, blank=False)
    power_id = models.IntegerField(verbose_name=u"Лошадиные силы",
                                   null=False, blank=False)

    # == Адреса ==
    formal_address = models.TextField(verbose_name=u"Адрес прописки", null=False, blank=False)
    real_address = models.TextField(verbose_name=u"Адрес прописки", null=False, blank=False)
    delivery_address = models.TextField(verbose_name=u"Адрес прописки", null=False, blank=False)
    
    class Meta:
        verbose_name = u"Страховой полис"
        verbose_name_plural = u"Страховые полисы"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.buy_date <= self.end_date:
            raise ValidationError(u'Конец периода страхования должен быть позже начала')
