# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):

    def __unicode__(self):
        return u'%s' % (self.body)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             blank=True,#если юзер анонимный
                             null=True)
    email = models.EmailField(max_length=75,
                            verbose_name = 'email')
    body = models.CharField(max_length=4096,
                            verbose_name='Содержание')
    sent_time = models.DateTimeField(auto_now=True,
                                     auto_now_add=True,
                                     verbose_name='Вопрос задан в')
    answered = models.BooleanField(default=False,
                                   verbose_name='Отвечен')

    def description(self):
        return '%s...' % (self.body[:128])

    
