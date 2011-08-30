# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField

class QuestionForm(forms.Form):
    body = forms.CharField(required=True,
                           label='Содержание вопроса',
                           widget=forms.Textarea(),)

class QuestionFormNotAuth(forms.Form):
    email = forms.EmailField(required=True, label='email')
    body = forms.CharField(required=True,
                          label='Содержание вопроса',
                          widget=forms.Textarea(),)
    captcha = CaptchaField()


class NotificationForm(forms.Form):
    
    sub = forms.CharField(required=True,
                          label='Тема сообщения',)
    body = forms.CharField(required=True,
                           label='Содержание сообщения',
                           widget=forms.Textarea(),)

class AnswerForm(forms.Form):
    def __init__(self,*args,**kwargs):
        body = ''
        if kwargs.has_key('body'):
            body = kwargs.pop('body')
        super(AnswerForm,self).__init__(*args,**kwargs)
        self.fields['body'] = forms.CharField(required=True,
                                              label='Содержание вопроса',
                                              widget=forms.Textarea(),
                                              initial=body)

        
