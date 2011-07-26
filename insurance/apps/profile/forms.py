# -*- coding: utf-8 -*-
import datetime
from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from profile.models import UserProfile,Persona



# Get list for SelectDateWidget()
year = datetime.datetime.now().year
years_list = range(year-100,year)

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('last_name', 'first_name', 'middle_name', 'birth_date')
        widgets = {
            'birth_date': SelectDateWidget(years=years_list),
        }

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

class PersonaForm(ModelForm):

    class Meta:
        model = Persona
        fields = ('last_name','first_name','middle_name','birth_date')
        widgets = {
            'birth_date': SelectDateWidget(years=years_list),
        }
