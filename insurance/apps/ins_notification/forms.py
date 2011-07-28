# -*- coding: utf-8 -*-
from django import forms

class QuestionForm(forms.Form):
    
    sub = forms.CharField(required=True,
                          label='Тема вопроса',)
    body = forms.CharField(required=True,
                           label='Содержание вопроса',
                           widget=forms.Textarea(),)

class NotificationForm(forms.Form):
    
    sub = forms.CharField(required=True,
                          label='Тема сообщения',)
    body = forms.CharField(required=True,
                           label='Содержание сообщения',
                           widget=forms.Textarea(),)

class AnswerForm(forms.Form):
    def __init__(self,*args,**kwargs):
        subject = ''
        if kwargs.has_key('subject'):
            subject = kwargs.pop('subject')
        body = ''
        if kwargs.has_key('body'):
            body = kwargs.pop('body')
        super(AnswerForm,self).__init__(*args,**kwargs)
        self.fields['subject'] = forms.CharField(required=True,
                                             label='Тема вопроса',
                                             initial=subject,)
        self.fields['body'] = forms.CharField(required=True,
                                              label='Содержание вопроса',
                                              widget=forms.Textarea(),
                                              initial=body)

        
