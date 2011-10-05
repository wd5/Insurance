# -*- coding: utf-8 -*-
from django.contrib import admin
from models import InsurancePolicy

class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'state',)
    readonly_fields = ("user", "type", "payment", "state", "company", "mark",
                       "model", "model_year", "power", "price", "wheel", "city",
                       "credit", "unlimited_users", "age", "experience_driving",
                       "age1", "experience_driving1", "age2",
                       "experience_driving2", "age3", "experience_driving3",
                       "vin", "body_type", "mileage", "last_name", "first_name",
                       "middle_name", "birth_date", "sex", "first_owner",
                       "reg_address", "liv_address", "pol_address")

admin.site.register(InsurancePolicy, InsurancePolicyAdmin)