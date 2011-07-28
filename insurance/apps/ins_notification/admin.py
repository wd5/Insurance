# -*- coding: utf-8 -*-
from django.contrib import admin
from ins_notification.models import Question
from profile.models import UserProfile
import sys

class QuestionAdmin(admin.ModelAdmin):
    list_display   = ('user_fio','subject','sent_time')
    list_filter = ('user',)
    search_fields = ['subject',]
    ordering = ('sent_time',)
    change_form_template = 'notification/admin_question_change_form.html'

    fieldsets = (
        (None, {
                'fields': ('subject','body')
                }),)
    readonly_fields = ('subject','body','sent_time')

    def user_fio(self,o):
        uprofile = UserProfile.objects.get(id=o.user.id)
        fio = "%s %s %s" % (uprofile.last_name,uprofile.first_name,uprofile.middle_name)
        return fio

    def change_view(self, request, object_id, extra_context=None):
        qws = Question.objects.get(id=object_id)
        
        uprofile = UserProfile.objects.get(id=qws.user.id)
        fio = "%s %s %s" % (uprofile.last_name,uprofile.first_name,uprofile.middle_name)
        extra_context = {
            'object_id': object_id,
            'fio':fio,
            'qws':qws,
        }
        return super(QuestionAdmin, self).change_view(request, object_id,
            extra_context=extra_context)

admin.site.register(Question,QuestionAdmin)



    
