# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from polices.models import CallRequests
from email_login.forms import PhoneNumberField
from captcha.fields import CaptchaField
from django.forms import ModelForm

class CallRequestForm(ModelForm):
    phone = PhoneNumberField()
    captcha = CaptchaField()
    comment = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = CallRequests
        exclude = ('user',)


