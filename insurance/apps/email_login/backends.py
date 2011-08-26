import re
from uuid import uuid4
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from registration.backends.default import *
from registration.models import RegistrationProfile

from forms import RegistrationForm

class RegistrationBackend(DefaultBackend):
    """
    Does not require the user to pick a username. Sets the username to a random
    string behind the scenes.
    
    """
    
    def register(self, request, **kwargs):
        email, password = kwargs['email'], kwargs['password1']
        
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(uuid4().get_hex()[:10], 
                                                                    email, password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_form_class(self, request):
        """
        Return the default form class used for user registration.
        
        """
        return RegistrationForm


# WE have EmailField in EmailAuthenticationForm. It`s realy need?
#email_re = re.compile(
#    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
#    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
#    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain
            
class AuthBackend(ModelBackend):
   def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username) #email field is unique => RegistrationForm...

            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
