# -*- coding: utf-8 -*-
import datetime
from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from profile.models import UserProfile,Persona
from email_login.forms import PhoneNumberField



# Get list for SelectDateWidget()
year = datetime.datetime.now().year
years_list = range(year-100,year)


class AdminUserBlockForm(ModelForm):
    reason_blocked = forms.CharField(widget=forms.TextInput(attrs={'size':'100', 'required':True}))
    class Meta:
        model = UserProfile
        fields = ('reason_blocked',)

    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        self.user = profile.user
        super(AdminUserBlockForm, self).__init__(instance=profile, *args, **kwargs)

    def save(self, commit=True):
        self.user.is_active = False
        if commit:
            self.user.save()
        return self.profile

class AdminUserMessageConfirmForm(forms.Form):
    subject = forms.CharField(label=u"Тема", min_length=10, max_length=100)
    message = forms.CharField(label=u"Уведомление", min_length=10, max_length=400, widget=forms.Textarea())


class AdminUserForm(ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'required', 'maxlength': 75}),
                             label=u"Адрес электронной почты")

    class Meta:
        model = User



class PersonaForm(ModelForm):
    phone = PhoneNumberField(label=u'Телефонный номер', required=False)
    class Meta:
        model = Persona
        exclude = ('user', 'me')


    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for f_name in self.fields:
            if f_name == 'phone':
                pass
            elif f_name == 'city_id':
                self.fields[f_name].widget.attrs['class'] = 'style_select'
            elif f_name in ('house', 'block', 'building', 'apartment'):
                self.fields[f_name].widget.attrs['class'] = 'style_input8a'
            else:
                self.fields[f_name].widget.attrs['class'] = 'style_input5'

                
class PassChangeForm(PasswordChangeForm):
    """
    Переопределены стили контролов в стандартной джанговской форме смены пароля.
    """
    def __init__(self, user, *args, **kwargs):
        super(PassChangeForm, self).__init__(user, *args, **kwargs)
        for f_name in self.fields:
            self.fields[f_name].widget.attrs['class'] = 'style_input5'
