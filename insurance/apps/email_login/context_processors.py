# -*- coding: utf-8 -*-

def context_regform(request):
    from forms import RegistrationForm
    from django.contrib.auth.forms import PasswordResetForm
    additions = {'reg_form': RegistrationForm(), 'reset_pass_form': PasswordResetForm()}
    return additions