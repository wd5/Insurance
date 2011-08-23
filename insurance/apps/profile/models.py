# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_ipgeobase.models import IPGeoBase



class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь', unique=True)

    # == Личные данные ==
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=30)
    first_name = models.CharField(verbose_name=u'Имя', max_length=30)
    middle_name = models.CharField(verbose_name=u'Отчество', max_length=30)

    # == Геолокация ==
    last_ip = models.CharField(verbose_name=u'Последний IP-адрес', max_length=15, null=True)
    city = models.CharField(verbose_name=u'Город по геолокации', max_length=100, null=True)

    # == Другое ==
    reason_blocked = models.CharField(verbose_name=u'Причина блокировки', max_length=100, null=True)

    class Meta:
        verbose_name = u"Профиль пользователя"
        verbose_name_plural = u"Профили пользователей"


@receiver(user_logged_in)
def save_ip(user, **kwargs):
    request = kwargs['request']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        # TODO: find out how this works with Apache/nginx
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.last_ip = ip
    ipgeobases = IPGeoBase.objects.by_ip(ip)
    if ipgeobases.exists():
        ipgeobase = ipgeobases[0]
        profile.city = ipgeobase.city
    profile.save()

class Persona(models.Model):
    user = models.ForeignKey(User)

    # == Адрес/контакты ==
    # TODO: Список городов брать из БД Вигена!
    city_id = models.IntegerField(verbose_name=u'Город', null=True, blank=True)
    address = models.TextField(verbose_name=u'Адрес', max_length=200, null=True, blank=True)
    phone = models.CharField(verbose_name=u'Телефонный номер', max_length=14, blank=True)   # TODO: phone number validation

    # == Фио ==
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=30)
    first_name = models.CharField(verbose_name=u'Имя', max_length=30)
    middle_name = models.CharField(verbose_name=u'Отчество', max_length=30)

    # == Другое ==
    comment = models.TextField(verbose_name=u"Комментарии", blank=True, null=True)

    # == Бизнес-логика ==
    me = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s' % (self.id,self.first_name)
    
    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

 
@receiver(post_save,sender=UserProfile)
def add_persona_himself(sender, **kwargs):
    """
    Добавить при регистрации персону - самого себя
    """
    user_profile = kwargs["instance"]
    user = user_profile.user
    try:
        user_persona = Persona.objects.get(user=user,me=True)
    except Persona.DoesNotExist:
        user_persona = Persona(user=user) # Создать новую запись
    user_persona.first_name = user_profile.first_name
    user_persona.last_name = user_profile.last_name
    user_persona.middle_name = user_profile.middle_name
    user_persona.me = True
    user_persona.save()
