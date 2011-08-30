# -*- coding: utf-8 -*-
from django.contrib import admin
from ins_notification.models import Question
from profile.models import UserProfile
import sys




class QuestionAdmin(admin.ModelAdmin):
    list_display   = ('user_fio','description','sent_time','answered')
    list_filter = ('user',)
    search_fields = ['body',]
    ordering = ('sent_time',)
    actions = ['mark_as_answered']
    change_form_template = 'notification/admin_question_change_form.html'

    fieldsets = (
        (None, {
                'fields': ('user','body','answered')
                }),)
    readonly_fields = ('user','body','sent_time','answered')

    def user_fio(self,o):
        uprofile = UserProfile.objects.get(id=o.user.id)
        fio = "%s %s %s" % (uprofile.last_name,uprofile.first_name,uprofile.middle_name)
        return fio

    def change_view(self, request, object_id, extra_context=None):
        fio = ''
        qws = Question.objects.get(id=object_id)
        if qws.user:
            uprofile = UserProfile.objects.get(id=qws.user.id)
            fio = "%s %s %s" % (uprofile.last_name,uprofile.first_name,uprofile.middle_name)
        extra_context = {
            'object_id': object_id,
            'fio':fio,
            'qws':qws,
        }
        return super(QuestionAdmin, self).change_view(request, object_id,
            extra_context=extra_context)

    def mark_as_answered(self, request, queryset):
        queryset.update(answered = True)
    mark_as_answered.short_description = "Mark selected questions as answered"

admin.site.register(Question,QuestionAdmin)



    
