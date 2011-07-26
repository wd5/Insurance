# -*- coding: utf-8 -*-
import datetime
from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from profile.models import UserProfile,Persona



class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('last_name', 'first_name', 'middle_name')

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

# Get list for SelectDateWidget()
year = datetime.datetime.now().year
years_list = range(year-100,year)

class PersonaForm(ModelForm):
    
    def __init__(self,*args,**kwargs):
        super(PersonaForm,self).__init__(*args,**kwargs)
        self.fields['persona_flag'] = forms.BooleanField(initial=True,
                                                         widget=forms.HiddenInput())
        if kwargs.has_key("instance"):
            persona_id = kwargs['instance'].id
        else:
            persona_id = None
        self.fields['persona_id'] = forms.CharField(required=False,
                                                    initial=persona_id,
                                                    widget=forms.HiddenInput())
        if persona_id:
            self.fields['me'] = forms.BooleanField(initial=kwargs['instance'].me,
                                                   required=False,
                                                   widget=forms.HiddenInput())
        else:
            self.fields['me'] = forms.BooleanField(initial=False,
                                                   required=False,
                                                   widget=forms.HiddenInput())

    class Meta:
        model = Persona
        fields = ('last_name','first_name','middle_name','birth_date','me')
        widgets = {
            'birth_date': SelectDateWidget(years=years_list),
        }
