from django.forms import ModelForm

from profile.models import UserProfile



class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address', 'phone')
