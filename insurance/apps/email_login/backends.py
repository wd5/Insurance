import re
from uuid import uuid4
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from registration.backends.default import *
from registration.models import RegistrationProfile
from profile.models import Persona

from forms import RegistrationForm

class RegistrationBackend(DefaultBackend):
    """
    Does not require the user to pick a username. Sets the username to a random
    string behind the scenes.

    """

    def register(self, request, **kwargs):
        email, password = kwargs['email'], kwargs.get('password1', None)

        if password is None:
            password = User.objects.make_random_password(length=8)

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = RegistrationProfile.objects.create_inactive_user(uuid4().get_hex()[:10],
                                                                    email, password, site)
        if kwargs.get('first_name'):
            new_user.first_name = kwargs.get('first_name')
        if kwargs.get('last_name'):
            new_user.last_name = kwargs.get('last_name')
        new_user.save()
        if kwargs.get('first_name') and kwargs.get('last_name') and kwargs.get('middle_name'):
            new_persona = Persona()
            new_persona.user = new_user
            new_persona.email = kwargs['email']
            new_persona.last_name = kwargs['last_name']
            new_persona.first_name = kwargs['first_name']
            new_persona.middle_name = kwargs['middle_name']
            new_persona.me = True
            if kwargs.get('phone'):
                new_persona.phone = kwargs['phone']
            new_persona.save()

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
