# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save

from django_ipgeobase.models import IPGeoBase



class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', unique=True)

    # Personal - got to do this, as you can't really change the User model
    last_name = models.CharField(verbose_name='Фамилия', max_length=30)
    first_name = models.CharField(verbose_name='Имя', max_length=30)
    middle_name = models.CharField(verbose_name='Отчество', max_length=30)

    # Arbitrary fields as a mockup
    address = models.TextField(verbose_name='Адрес пользователя', max_length=200, blank=True)
    phone = models.CharField(verbose_name='Телефонный номер', max_length=14, blank=True)   # TODO: phone number validation

    # Geolocation-related
    last_ip = models.CharField(verbose_name='Последний IP-адрес', max_length=15, null=True)
    city = models.CharField(verbose_name='Город по геолокации', max_length=100, null=True)
    reason_blocked = models.CharField(verbose_name='Причина блокировки', max_length=100, null=True)

    class Meta:
        verbose_name = u"Профиль пользователя"
        verbose_name_plural = u"Профили пользователей"


@receiver(user_logged_in)
def save_ip(user, **kwargs):
    request = kwargs['request']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        # TODO: find out how this works with Apache/nginx
        ip = request.META['HTTP_X_FORWARDED_FOR']
        print ">>>>>>>>>>", ip
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
    last_name = models.CharField(verbose_name='Фамилия', max_length=30)
    first_name = models.CharField(verbose_name='Имя', max_length=30)
    middle_name = models.CharField(verbose_name='Отчество', max_length=30)
    birth_date = models.DateField(blank=True)
    me = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s' % (self.id,self.name)
    
    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

 
@receiver(post_save,sender=UserProfile)
def add_persona(sender, **kwargs):
    import sys
    print >> sys.stderr, "add_persona(sender, **kwargs):"
    print >> sys.stderr, "sender =", kwargs["instance"].user.email
    user_id = kwargs["instance"].user.id
    print >> sys.stderr, "user_id =", user_id
