# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from django_ipgeobase.models import IPGeoBase



class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    # Personal - got to do this, as you can't really change the User model
    last_name = models.CharField(name='Фамилия', max_length=30, blank=True)
    first_name = models.CharField(name='Имя', max_length=30, blank=True)
    middle_name = models.CharField(name='Отчество', max_length=30, blank=True)

    # Arbitrary fields as a mockup
    address = models.TextField(name='Адрес пользователя', max_length=200, blank=True)
    phone = models.CharField(name='Телефонный номер', max_length=14, blank=True)   # TODO: phone number validation

    # Geolocation-related
    last_ip = models.CharField(name='Последний IP-адрес', max_length=15, null=True)
    city = models.CharField(name='Город по геолокации', max_length=100, null=True)
    reason_blocked = models.CharField(name='Причина блокировки', max_length=100, null=True)

@receiver(user_logged_in)
def save_ip(user, **kwargs):
    request = kwargs['request']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        # TODO: find out how this works with Apache
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
