# -*- coding: utf-8 -*-

def context_regform(request):
    from forms import RegistrationForm
    additions = {'reg_form': RegistrationForm(),}
    return additions