# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage    
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template

from polices.models import InsurancePolicy, TYPE_CHOICES
from ins_notification.forms import QuestionForm
from ins_notification.models import Question

from forms import PersonaForm, PassChangeForm
from models import Persona

@login_required
def profile(request):
    """
    Страница /profile/ - редактирование осн. персоны пользователя,
    а также смена его пароля и кнопка добавления доп. персон.
    """
    user = request.user
    try:
        main_persona = Persona.objects.get(user=user, me=True)
    except ObjectDoesNotExist:
        main_persona = None
    personas = Persona.objects.filter(user=user, me=False)
#    password_form = PasswordChangeForm(user)
    password_form = PassChangeForm(user)

    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=main_persona)
        if form.is_valid():
            persona = form.save(commit=False)
            persona.user = user
            persona.me = True
            if form.cleaned_data.get("phone") is None:  # hack.
                persona.phone = ""
            persona.save()
            return HttpResponseRedirect(reverse('userprofile_edit'))
    else:
        form = PersonaForm(instance=main_persona)
    return direct_to_template(request, 'profile/userprofile_base2.html', {'persona_form': form, 'personas': personas,
                                                                          'main_persona': main_persona,
                                                                          'password_form': password_form})

@login_required
def edit_persona(request, persona_id):
    user = request.user
    personas = Persona.objects.filter(user=user, me=False)
    persona = get_object_or_404(Persona, pk=persona_id)
    main_persona = Persona.objects.get(user=user, me=True)
    if persona == main_persona:
        return HttpResponseRedirect(reverse('userprofile_edit'))
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            cd = form.cleaned_data
            pers = form.save(commit=False)
            if cd.get("phone") is None:  # hack.
                pers.phone = ""
            pers.save()
            return HttpResponseRedirect(reverse('userprofile_editpersona', kwargs={"persona_id": pers.id}))
    else:
        form = PersonaForm(instance=persona)
    return direct_to_template(request, 'profile/userprofile_editpersona.html', {'persona_form': form, 'personas': personas,
                                                                               'persona': persona,
                                                                               'main_persona': main_persona})


@login_required
def add_persona(request):
    user = request.user
    personas = Persona.objects.filter(user=user, me=False)
    main_persona = Persona.objects.get(user=user, me=True)
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            pers = form.save(commit=False)
            pers.user = user
            if cd.get("phone") is None:  # hack.
                pers.phone = ""
            pers.save()
            return HttpResponseRedirect(reverse('userprofile_editpersona', kwargs={"persona_id": pers.id}))
    else:
        form = PersonaForm()
    return direct_to_template(request, 'profile/userprofile_addpersona.html', {'persona_form': form, 'personas': personas,
                                                                               'main_persona': main_persona})


@login_required
def delete_persona(request, persona_id):
    # TODO: Removal confirmation 
    persona = get_object_or_404(Persona, pk=persona_id, me=False)
    persona.delete()
    return HttpResponseRedirect(reverse('userprofile_edit'))


@login_required
def policy_list(request, policy_type=None):
    policy_types = dict(TYPE_CHOICES)
    if not policy_type:
        policy_type, _ = TYPE_CHOICES[0] #InsurancePolicy.TYPE_CHOICES[0]
    user = request.user
    #TODO: персоны!!!!
    #personas = user.persona_set.all()
    #print personas
    query = InsurancePolicy.objects.filter(user=user, type=policy_type)
    print query
    extra_context = {
        "policy_type": policy_type,
        "policy_types": policy_types,
    }
    context = {
        "template_name": "profile/userprofile_policylist.html",
        "queryset": query,
        "template_object_name": "policy",
        "extra_context": extra_context,
    }
    return object_list(request, **context)

@login_required
def faq(request):
    context = {}
    flatpage = FlatPage.objects.get(title='FAQ')
    form = QuestionForm(request.POST or None)
    sent = False
    if form.is_valid():
        o = Question()
        o.user = request.user
        o.subject = form.cleaned_data['sub']
        o.body = form.cleaned_data['body']
        o.save()
        sent = True
    context = {
        'sent':sent,
        'flatpage': flatpage,
        'question_form': form
    }
    return render_to_response('profile/userprofile_faq.html',
                              context,
                              context_instance=RequestContext(request))

