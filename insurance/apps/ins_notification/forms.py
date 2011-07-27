# -*- coding: utf-8 -*-
from django import forms

class QuestionForm(forms.Form):
    
    sub = forms.CharField(required=True,
                          label='Тема вопроса',)
    body = forms.CharField(required=True,
                           label='Содержание вопроса',
                           widget=forms.Textarea(),
                           )



