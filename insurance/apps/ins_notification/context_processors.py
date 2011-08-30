# -*- coding: utf-8 -*-
from ins_notification.forms import QuestionForm, QuestionFormNotAuth

def questions(request):
    if request.user.is_authenticated():
        quest_form = QuestionForm()
    else:
        quest_form = QuestionFormNotAuth()

    return {'form':quest_form}
