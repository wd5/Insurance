from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django import forms

from notification.models import NoticeSetting, Notice, ObservedItem, NoticeQueueBatch

class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'medium', 'send')

class NoticeAdminForm(forms.ModelForm):
    """
    Custom AdminForm to enable messages to groups and all users.
    """
    sender = forms.ModelChoiceField(label=_('Sender'), queryset=User.objects.all(), required=False)
    recipient = forms.ModelChoiceField(label=_('Recipients'), queryset=User.objects.all(), required=False)
    sub = forms.CharField(label=_('Subject'), required=True)

    def __init__(self, *args, **kwargs):
        super(NoticeAdminForm, self).__init__(*args, **kwargs)
        self.fields['on_site'].initial = True
        
#        if 'initial' in kwargs:
#            ids = kwargs['initial']['ids']
#            self.ids = ids.split(',')
#            self.users = User.objects.filter(pk__in=self.ids)
#            self.fields['recipient'].choices = self._get_recipient_choices()
#    
#    def _get_recipient_choices(self):
#        user_list = ''
#        for user in self.users:
#            user_list = '%s,%s' % (user, user_list)
#        return [('ids', '%s' % user_list),] + \
#               [(user.pk, user.email) for user in User.objects.all()]
#    


    class Meta:
        model = Notice
        exclude = ('archived', 'unseen')

class NoticeAdmin(admin.ModelAdmin):
    form = NoticeAdminForm
    list_display = ('sub','message', 'recipient_email', 'sender_email', 'added', 'unseen', 'archived')

    def recipient_email(self,o):
        uprofile = User.objects.get(id=o.recipient.id)
        email = '%s' % (uprofile.email)
        return email
        
    def sender_email(self,o):
        uprofile = User.objects.get(id=o.recipient.id)
        email = '%s' % (uprofile.email)
        return email

    def save_model(self, request, obj, form, change):
        """
        Saves the message for the recipient and looks in the form instance
        for other possible recipients. Prevents duplication by excludin the
        original recipient from the list of optional recipients.

        When changing an existing message and choosing optional recipients,
        the message is effectively resent to those users.
        """
        ids = request.GET.get('ids')
        if ids:
            ids = ids.split(',')
            recipients = User.objects.filter(pk__in = ids)
            for recipient in recipients:
                obj.pk = None
                obj.sender = None
                obj.recipient = recipient
                obj.save()

admin.site.register(NoticeQueueBatch)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(ObservedItem)
