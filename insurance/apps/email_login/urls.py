from django.conf.urls.defaults import *
from django.contrib.auth.views import login
from django.views.generic.simple import direct_to_template

from registration.views import activate, register

from email_login.forms import AuthenticationForm



urlpatterns = patterns('',
                       url(r'^activate/complete/$', direct_to_template,
                           { 'template': 'registration/activation_complete.html' },
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$', activate,
                           { 'backend': 'email_login.backends.RegistrationBackend' },
                           name='registration_activate'),
                       url(r'^register/$', register,
                           { 'backend': 'email_login.backends.RegistrationBackend' },
                           name='registration_register'),
                       url(r'^login/$', login,
                           { 'template_name': 'registration/login.html',
                             'authentication_form': AuthenticationForm },
                           name='auth_login'),
                       (r'', include('registration.backends.default.urls')),
                       )
