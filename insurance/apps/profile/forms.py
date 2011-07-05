from django.forms import ModelForm
from django.contrib.auth.models import User

from profile.models import UserProfile



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address', 'phone')
