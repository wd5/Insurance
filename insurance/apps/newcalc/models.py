# -*- coding: utf-8 -*-
from django.db import models


class Mark(models.Model):
    """
    Марка автомобиля.
    """
    mark_id = models.IntegerField(primary_key=True)
    mark_name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.mark_name

    class Meta:
        db_table = u'mark'
        managed = False
        ordering = ("mark_name",)


class Model(models.Model):
    """
    Модель автомобиля.
    """
    model_id = models.IntegerField(primary_key=True)
    model_name = models.CharField(max_length=50)
    model_mark = models.ForeignKey(Mark, db_column="model_mark")
    model_active = models.IntegerField(default=1)

    def __unicode__(self):
        return self.model_name

    class Meta:
        db_table = u'model'
        managed = False


class ModelYear(models.Model):
    """
    Годы выпуска автомобилей.
    """
    year_id = models.IntegerField(primary_key=True)
    model_year_id = models.ForeignKey(Model, db_column="model_year_id")
    model_year_year = models.PositiveIntegerField()

    def __unicode__(self):
        return "%d" % self.model_year_year

    class Meta:
        db_table = u'model_year'
        managed = False


class Mym(models.Model):
    mym_y = models.ForeignKey(ModelYear, db_column="mym_y")
    mym_m = models.ForeignKey(Model, db_column="mym_m")
    mym_id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = u'mym'


class Power(models.Model):
    """
    Мощность двигателя.
    """
    power_id = models.IntegerField(primary_key=True)
    power_name = models.CharField(max_length=20)
    power_mym = models.ForeignKey(Mym, db_column="power_mym")

    def __unicode__(self):
        return self.power_name

    class Meta:
        db_table = u'power'
        managed = False


class Price(models.Model):
    """
    Цена автомобиля.
    """
    price_id = models.IntegerField(primary_key=True)
    price_mym = models.ForeignKey(Mym, db_column="price_mym")
    price_min = models.FloatField()
    price_max = models.FloatField()
    price_power = models.ForeignKey(Power, db_column="price_power")

    class Meta:
        db_table = u'price'
        managed = False


class City(models.Model):
    """
    Населенные пункты.
    """
    city_id = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.city_name

    class Meta:
        db_table = u'city'
        managed = False


class BurglarAlarm(models.Model):
    """
    Производители и модели сигнализаций.
    """
    burglar_alarm_id = models.IntegerField(primary_key=True)
    burglar_alarm_name = models.CharField(max_length=50)
    burglar_alarm_parent = models.ForeignKey('self',
                                             db_column="burglar_alarm_parent",
                                             related_name="models")

    def __unicode__(self):
        return self.burglar_alarm_name

    class Meta:
        db_table = u'burglar_alarm'
        managed = False
        ordering = ["burglar_alarm_name",]


class Company(models.Model):
    """
    Страховые компании.
    """
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=50)
    company_full_name = models.CharField(max_length=100)
    company_block = models.SmallIntegerField()
    company_alias = models.CharField(max_length=50)
    company_comment = models.CharField(max_length=255)
    class Meta:
        db_table = u'company'
        managed = False


class InsuranceType(models.Model):
    insurance_type_id = models.IntegerField(primary_key=True)
    insurance_type_name = models.CharField(max_length=150)
    insurance_type_block = models.IntegerField()
    class Meta:
        db_table = u'insurance_type'

class CompanyCondition(models.Model):
    company_condition_id = models.IntegerField(primary_key=True)
    company_condition_company = models.IntegerField()
    company_condition_insurance = models.IntegerField()
    company_condition_comment = models.CharField(max_length=255)
    class Meta:
        db_table = u'company_condition'
        managed = False

        #class KackoIt(models.Model):

#    kacko_it_it = models.IntegerField(db_column='KACKO_it_it') # Field name made lowercase.
#    kacko_it_kp = models.IntegerField(db_column='KACKO_it_Kp') # Field name made lowercase.
#    kacko_it_company = models.IntegerField(db_column='KACKO_it_company') # Field name made lowercase.
#    class Meta:
#        db_table = u'KACKO_it'
#
class KackoParameters(models.Model):
    kparameter_id = models.IntegerField(primary_key=True)
    kparameter_name = models.CharField(max_length=765, blank=True)
    kparameter_description = models.CharField(max_length=3000, blank=True)
    kparameter_alias = models.CharField(max_length=765)
    kparameter_comment = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = u'KACKO_parameters'
        managed = False
#
#
#class Cf(models.Model):
#    cf_c = models.IntegerField()
#    cf_f = models.IntegerField()
#    cf_v = models.FloatField()
#    class Meta:
#        db_table = u'cf'
#

#
#class ClassKbm(models.Model):
#    class_kbm_id = models.IntegerField(primary_key=True)
#    class_kbm_name = models.CharField(max_length=60)
#    class_kbm_value = models.FloatField()
#    class Meta:
#        db_table = u'class_kbm'
#
#class Coefficient(models.Model):
#    coefficient_company = models.IntegerField()
#    coefficient_factors = models.IntegerField()
#    coefficient_place = models.IntegerField()
#    coefficient_value = models.FloatField()
#    coefficient_insurance_type = models.IntegerField()
#    class Meta:
#        db_table = u'coefficient'
#
#class Commision(models.Model):
#    commision_company = models.IntegerField()
#    commision_insurance_type = models.IntegerField()
#    commision_percent = models.FloatField()
#    class Meta:
#        db_table = u'commision'
#

#
#class Factors(models.Model):
#    factor_id = models.IntegerField(primary_key=True)
#    factor_name = models.CharField(max_length=150)
#    factor_value = models.FloatField()
#    class Meta:
#        db_table = u'factors'
#
#
#
#
#

#

#

#
#class Tasks(models.Model):
#    task_id = models.IntegerField(primary_key=True)
#    task_name = models.CharField(max_length=150)
#    task_text = models.CharField(max_length=3000)
#    task_user = models.IntegerField()
#    task_execute = models.IntegerField()
#    task_add = models.DateTimeField()
#    class Meta:
#        db_table = u'tasks'
#
#class Towns(models.Model):
#    town_id = models.IntegerField(primary_key=True)
#    town_name = models.CharField(max_length=150)
#    class Meta:
#        db_table = u'towns'
#
#class UserType(models.Model):
#    user_type_id = models.IntegerField(primary_key=True)
#    user_type_name = models.CharField(max_length=150)
#    user_type_value = models.IntegerField()
#    class Meta:
#        db_table = u'user_type'
#
#class Users(models.Model):
#    user_id = models.IntegerField(primary_key=True)
#    user_name = models.CharField(max_length=60)
#    user_password = models.CharField(max_length=60)
#    user_email = models.CharField(max_length=90)
#    user_fullname = models.CharField(max_length=150)
#    user_type = models.IntegerField()
#    user_block = models.IntegerField()
#    user_registration = models.DateTimeField()
#    user_lastvisit = models.DateTimeField()
#    class Meta:
#        db_table = u'users'

class Property(models.Model):
    property_id = models.IntegerField(primary_key=True)
    property_name = models.CharField(max_length=50)
    property_comment = models.CharField(max_length=255)

    class Meta:
        db_table = u'property'

    def __unicode__(self):
        return self.property_name


class PropertyParameters(models.Model):
    pparameter_id = models.IntegerField(primary_key=True)
    pparameter_name = models.CharField(max_length=255, blank=True)
    pparameter_alias = models.CharField(max_length=255)
    pparameter_comment = models.CharField(max_length=1000)
    pparameter_active = models.BooleanField(default=True)
    class Meta:
        db_table = u'property_parameters'
        managed = False


class TripType(models.Model):
    trip_type_id = models.IntegerField(primary_key=True)
    trip_type_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.trip_type_name

    class Meta:
        db_table = u'trip_type'
        managed = False


class TripPurpose(models.Model):
    trip_purpose_id = models.IntegerField(primary_key=True)
    trip_purpose_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.trip_purpose_name

    class Meta:
        db_table = u'trip_purpose'
        managed = False
