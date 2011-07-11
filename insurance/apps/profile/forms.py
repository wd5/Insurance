from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

from profile.models import UserProfile



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address', 'phone')

class AdminUserBlockForm(ModelForm):
    reason_blocked = forms.CharField(widget=forms.TextInput(attrs={'size':'100', 'required':True}))
    class Meta:
        model = UserProfile
        fields = ('reason_blocked',)

    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        self.user = profile.user
        super(AdminUserBlockForm, self).__init__(instance=profile, *args, **kwargs)

    def save(self, commit=True):
        self.user.is_active = False
        if commit:
            self.profile.save()
            self.user.save()
        return self.profile
