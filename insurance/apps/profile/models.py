# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_ipgeobase.models import IPGeoBase

CITY_CHOICES = ((0, "Москва"), (1, "Московская обл."))



class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь', unique=True)

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
    last_name = models.CharField(verbose_name=u'*Фамилия', max_length=30)
    first_name = models.CharField(verbose_name=u'*Имя', max_length=30)
    middle_name = models.CharField(verbose_name=u'*Отчество', max_length=30)
    email = models.EmailField(verbose_name=u'E-mail', blank=True)
    phone = models.CharField(verbose_name=u'Телефонный номер', max_length=14, blank=True)
    # TODO: Список городов брать из БД Вигена!
    city_id = models.IntegerField(verbose_name=u'Город', null=True, blank=True, choices=CITY_CHOICES)
    zip_code = models.CharField(verbose_name=u'Индекс', blank=True, max_length=6)
    street = models.CharField(verbose_name=u'Улица', blank=True, max_length=100)
    house = models.CharField(verbose_name=u'Дом', blank=True, max_length=3)
    block = models.CharField(verbose_name=u'Корпус', blank=True, max_length=2)
    building = models.CharField(verbose_name=u'Строение', blank=True, max_length=2)
    apartment = models.CharField(verbose_name=u'Квартира', blank=True, max_length=3)
    comment = models.TextField(verbose_name=u"Дополнительная информация", blank=True, null=True)
    me = models.BooleanField(verbose_name=u"Основная персона пользователя", default=False)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    
    def get_full_address(self):
        street_str = u""
        if self.zip_code:
            street_str = u"%s, " % self.zip_code
        if self.street:
            street_str = u"%s%s, " % (street_str, self.street)
        if self.house:
            street_str = u"%sд.%s, " % (street_str, self.house)
        if self.block:
            street_str = u"%sкорп.%s, " % (street_str, self.block)
        if self.building:
            street_str = u"%sстр.%s, " % (street_str, self.building)
        if self.apartment:
            street_str = u"%sкв.%s, " % (street_str, self.apartment)
        street_str = u"%s%s %s %s" % (street_str, self.last_name, self.first_name,
                                     self.middle_name)
        return street_str
    
    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"
        ordering = ('user',)


@receiver(post_save, sender=Persona)
def update_user_info(sender, **kwargs):
    """
    При изменении данных осн. персоны - обновлять ФИО у User.
    """
    persona = kwargs["instance"]
    if persona.me:
        persona.user.last_name = persona.last_name
        persona.user.first_name = persona.first_name
        persona.user.save()

def show_user_ident(user):
    using_persona = False
    try:
        persona = Persona.objects.get(user=user, me=True)
    except Persona.DoesNotExist:
        using_persona = False
    if using_persona and persona.last_name:
        ident = "%s %s %s" % (persona.last_name,persona.first_name,persona.middle_name)
        using_persona = True

    if not using_persona:
        ident = user.email
    return ident
    
#Легкий манки-патчинг для вывода везде мыла в качестве юзернейма =)
User.__unicode__ = show_user_ident
