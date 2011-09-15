from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django import forms

from notification.models import NoticeSetting, Notice, ObservedItem, NoticeQueueBatch

class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ('label', 'display', 'description', 'default')

class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'medium', 'send')

class NoticeAdminForm(forms.ModelForm):
    """
    Custom AdminForm to enable messages to groups and all users.
    """
    sender = forms.ModelChoiceField(label=_('Sender'), queryset=User.objects.all(), required=False)
    sub = forms.CharField(label=_('Subject'), required=True)
    group = forms.ChoiceField(label=_('group'), required=False,
        help_text=_('Creates the message optionally for all users or a group of users.'))

    def __init__(self, *args, **kwargs):
        super(NoticeAdminForm, self).__init__(*args, **kwargs)
        self.fields['group'].choices = self._get_group_choices()
        self.fields['on_site'].initial = True

    def _get_group_choices(self):
        return [('', u'---------'), ('all', _('All users'))] + \
            [(group.pk, group.name) for group in Group.objects.all()]
    
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
        obj.save()
        
        if form.cleaned_data['group'] == 'all':
            # send to all users
            recipients = User.objects.exclude(pk=obj.recipient.pk)
        else:
            # send to a group of users
            recipients = []
            group = form.cleaned_data['group']
            if group:
                group = Group.objects.get(pk=group)
                recipients.extend(
                    list(group.user_set.exclude(pk=obj.recipient.pk)))
        # create messages for all found recipients
        for user in recipients:
            obj.pk = None
            obj.recipient = user
            obj.save()

admin.site.register(NoticeQueueBatch)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(ObservedItem)
