# -*- coding: utf-8 -*-
from django.contrib import admin
from models import InsurancePolicy, CallRequests

class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'state',)
    readonly_fields = ("user", "type", "payment", "state", "company", "mark",
                       "model", "model_year", "power_str", "price", "wheel", "city",
                       "credit", "unlimited_users", "age", "experience_driving",
                       "age1", "experience_driving1", "age2",
                       "experience_driving2", "age3", "experience_driving3",
                       "first_name", "last_name", "middle_name", "birth_date",
                       "sex", "category", "citizenship", "passport_series",
                       "passport_number", "issued_org", "issued_date",
                       "reg_region", "reg_area", "reg_city", "reg_street",
                       "reg_index", "reg_building", "reg_housing", "reg_flat",
                       "live_region", "live_area", "live_city", "live_street",
                       "live_index", "live_building", "live_housing", "live_flat",
                       "vin", "number", "body_number", "body_type", "pts_number",
                       "pts_date", "power", "volume", "mileage", "kpp", "motor",
                       "owner_last_name", "owner_first_name",
                       "owner_middle_name", "owner_birth_date", "first_owner",
                       "owner_sex", "date", "time", "street", "building",
                       "structure", "housing", "floor", "domophone", "flat",
                       "porch", "payments", "comment"
                      )

class CallRequestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'comment', 'date')

admin.site.register(CallRequests, CallRequestsAdmin)
admin.site.register(InsurancePolicy, InsurancePolicyAdmin)
