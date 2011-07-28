# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):

    def __unicode__(self):
        return u'%s' % (self.subject)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    user = models.ForeignKey(User,
                             verbose_name='Пользователь')
    subject = models.CharField(max_length=512,
                               blank=True,
                               null='True',
                               verbose_name='Тема')
    body = models.CharField(max_length=4096,
                            blank=True,
                            null='True',
                            verbose_name='Содержание')
    sent_time = models.DateTimeField(auto_now=True,
                                     auto_now_add=True,)

    
