# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

from captcha.fields import CaptchaField

attrs_dict = { 'class': 'required' }

class PhoneNumberWidget(forms.MultiWidget):
    def __init__(self,attrs=None):
        wigs = (forms.TextInput(attrs={'size': '3', 'maxlength': '3'}), forms.TextInput(attrs={'size': '7', 'maxlength':'7'}))
        super(PhoneNumberWidget, self).__init__(wigs, attrs)

    def decompress(self, value):
        if value:
            return [value[:3], value[3:]]
        else:
            return [None, None]

    def format_output(self, rendered_widgets):
        return "%s%s" % (rendered_widgets[0], rendered_widgets[1])

class PhoneNumberField(forms.MultiValueField):
    widget = PhoneNumberWidget
    def __init__(self, *args, **kwargs):
        fields=(forms.CharField(min_length=3, max_length=3), forms.CharField(min_length=7, max_length=7))
        super(PhoneNumberField, self).__init__(fields, *args, **kwargs)
    def compress(self, data_list):
        if data_list:
            try:
                return "%03d%07d" % (int(data_list[0]), int(data_list[1]))
            except ValueError:
                return ""
        else:
            return None


class RegistrationForm(forms.Form):
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)
    middle_name = forms.CharField(required=False, max_length=30)
    phone = PhoneNumberField(required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))

    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={ 'required': _("You must agree to the terms to register") })
    captcha = CaptchaField()
    email.widget.attrs['class'] = 'style_input5'
    password1.widget.attrs['class'] = 'style_input5'
    password2.widget.attrs['class'] = 'style_input5'
    captcha.widget.attrs['class'] = 'style_input5'
    first_name.widget.attrs['class'] = 'style_input5'
    last_name.widget.attrs['class'] = 'style_input5'
    middle_name.widget.attrs['class'] = 'style_input5'

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']
    def clean_phone(self):
        if self.cleaned_data['phone'] == "":
            raise forms.ValidationError("Недопустимые символы в номере телефона.")
        return self.cleaned_data['phone']


class EmailAuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.EmailField(label=_("Email"), max_length=75)
