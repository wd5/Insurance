# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from notification.models import Notice,send
from ins_notification.forms import QuestionForm


@login_required
def inbox(request):
    notices = Notice.objects.notices_for(request.user, sent=True)
    
    extra_content = {'notices':notices}
    return direct_to_template(request,
                              'notification/inbox.html',
                              extra_content)


@login_required
def question(request):
    quest_form = QuestionForm(request.POST or None)
    sent = False
    if quest_form.is_valid():
        extra_context =  {'sub':quest_form.cleaned_data["sub"],
                          
                          'now':True,}
        send(user,'is_question',
             extra_context=extra_context,
             sender=request.user,
             on_site=True)
        sent = True
    extra_content = {'quest_form': quest_form,
                     'sent':sent}
    return direct_to_template(request, 
                              'notification/question.html',
                              extra_content)



