# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from polices.forms import CallRequestForm
from email_login.backends import RegistrationBackend

def create_call_request(request):
    call_form = CallRequestForm(request.POST or None)
    if call_form.is_valid():
        form = call_form.save(commit=False)
        if request.user.is_authenticated:
            form.user = request.user
        form.save()
        return redirect(reverse('ncalc_step3'))
    return direct_to_template(request, 'call_request.html', {'call_form': call_form})
