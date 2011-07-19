# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User



class InsurancePolicy(models.Model):
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

    user = models.ForeignKey(User)

    buy_date = models.DateField(verbose_name=u"Время начала действия", null=True)
    end_date = models.DateField(verbose_name=u"Время окончания действия", null=True)
    type = models.SmallIntegerField(verbose_name=u"Тип полиса", null=False, blank=False,
                               choices=TYPE_CHOICES)
    payment = models.CharField(verbose_name=u"Оплата", max_length=10, null=False, blank=False, default="unpayed",
                               choices=PAYMENT_CHOICES)
    state = models.CharField(verbose_name=u"Статус полиса", max_length=10, null=False, blank=False, default="init",
                             choices=STATE_CHOICES)
    
    class Meta:
        verbose_name = u"Страховой полис"
        verbose_name_plural = u"Страховые полисы"
