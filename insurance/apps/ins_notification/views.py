# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from notification.models import Notice
from profile.models import UserProfile

from ins_notification.forms import AnswerForm
from ins_notification.forms import QuestionForm
from ins_notification.models import Question



import sys

@login_required
def inbox(request):
    notices = Notice.objects.filter(recipient=request.user)
    extra_content = {'notices':notices}
    return direct_to_template(request,
                              'notification/inbox.html',
                              extra_content)

@login_required
def question(request):
    quest_form = QuestionForm(request.POST or None)
    sent = False
    if quest_form.is_valid():
        o = Question()
        o.user = request.user
        o.subject = quest_form.cleaned_data['sub']
        o.body = quest_form.cleaned_data['body']
        o.save()
        sent = True
    extra_content = {'quest_form': quest_form,
                     'sent':sent}
    return direct_to_template(request, 
                              'notification/question.html',
                              extra_content)

@staff_member_required
def answer(request,q_id):
    qws = Question.objects.get(id=q_id)
    user = qws.user
    uprofile = UserProfile.objects.get(id=qws.user.id)
    fio = "%s %s %s" % (uprofile.last_name,uprofile.first_name,uprofile.middle_name)
    sent = False
    if(request.POST):
        answ_form = AnswerForm({'subject':request.POST['subject'],
                                'body':request.POST['body']})
        if answ_form.is_valid():
            user.email_user(answ_form.cleaned_data['subject'],
                            answ_form.cleaned_data['body'],
                            from_email="admin@directif.ru"
            )
            sent = True
            print >> sys.stderr, "q_id =", q_id
            qws.answered = True
            qws.save()
    else:
        subject = 'Re: ' + qws.subject
        body = u"\n\n\nВы спрашивали:\n-----\n" + qws.body
        answ_form = AnswerForm(subject=subject,body=body)
    extra_content = {'answ_form':answ_form,
                     'qwestion':qws,
                      'fio':fio,
                     'sent':sent,
                     'user':user}
    return direct_to_template(request, 
                              'notification/admin_question_answer_letter.html',
                              extra_content)

def ins_single(request,n_id):
    notice = Notice.objects.get(id=n_id)
    extra_content = {'notice':notice}
    return direct_to_template(request, 
                              'notification/ins_single.html',
                              extra_content)
    
    

