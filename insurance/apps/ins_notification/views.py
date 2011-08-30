# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from notification.models import Notice
from profile.models import UserProfile

from ins_notification.forms import AnswerForm
from ins_notification.forms import QuestionForm, QuestionFormNotAuth
from ins_notification.models import Question



import sys

@login_required
def inbox(request):
    notices = Notice.objects.filter(recipient=request.user)
    extra_content = {'notices':notices}
    return direct_to_template(request,
                              'notification/inbox.html',
                              extra_content)

def question(request):
    if request.user.is_authenticated():
        quest_form = QuestionForm(request.POST or None)
    else:
        quest_form = QuestionFormNotAuth(request.POST or None)
    sent = False
    if quest_form.is_valid():
        o = Question()
        if request.user.is_authenticated():
            o.user = request.user
            o.email = request.user.email
        else:
            o.user = None
            o.email = quest_form.cleaned_data['email']
        o.body = quest_form.cleaned_data['body']
        o.save()
        sent = True
        return HttpResponseRedirect(reverse('question_success'))
    extra_content = {'form': quest_form,
                     'sent':sent}
    return render_to_response('notification/question.html',
                              extra_content,
                              context_instance=RequestContext(request))

@staff_member_required
def answer(request,q_id):
    qws = Question.objects.get(id=q_id)
    user = qws.user
    uprofile = UserProfile.objects.get(id=qws.user.id)
    fio = "%s %s %s" % (uprofile.last_name,uprofile.first_name,uprofile.middle_name)
    sent = False
    if(request.POST):
        answ_form = AnswerForm({'body':request.POST['body']})
        if answ_form.is_valid():
            # TODO: from_email should not be hardcoded!
            user.email_user('Re: directif.ru',
                            answ_form.cleaned_data['body'],
                            from_email=" admin@polisbook.ru"
            )
            sent = True
            print >> sys.stderr, "q_id =", q_id
            qws.answered = True
            qws.save()
    else:
        body = u"\n\n\nВы спрашивали:\n-----\n" + qws.body
        answ_form = AnswerForm(body=body)
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
    
    

