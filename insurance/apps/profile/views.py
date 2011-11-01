# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template

from polices.models import InsurancePolicy
from polices.models import TYPE_CHOICES, STATUS_PAYMENT_CHOICES, STATE_CHOICES
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
        main_persona.full_name = u"%s %s" % (main_persona.first_name, main_persona.last_name)
    except ObjectDoesNotExist:
        main_persona = None
    personas = Persona.objects.filter(user=user, me=False)
    for p in personas:
        p.full_name = u"%s %s" % (p.first_name, p.last_name)
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
    for p in personas:
        p.full_name = u"%s %s" % (p.first_name, p.last_name)
    main_persona = Persona.objects.get(user=user, me=True)
    if persona == main_persona:
        return HttpResponseRedirect(reverse('userprofile_edit'))
    main_persona.full_name = u"%s %s" % (main_persona.first_name, main_persona.last_name)
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
    for p in personas:
        p.full_name = u"%s %s" % (p.first_name, p.last_name)
    main_persona = Persona.objects.get(user=user, me=True)
    main_persona.full_name = u"%s %s" % (main_persona.first_name, main_persona.last_name)
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
        return redirect(reverse("userprofile_policylist_type", args=[policy_type,]))
    user = request.user
    #TODO: персоны!!!!
    #personas = user.persona_set.all()
    #print personas
    query = InsurancePolicy.objects.filter(user=user, type=policy_type)
    for q in query:
        q.state = dict(STATE_CHOICES)[q.state]
        q.vehicle = u"%s %s (%s г.)" % (q.mark, q.model, q.model_year)

    print query
    extra_context = {
        "policy_list": query,
        "policy_type": policy_type,
        "policy_types": policy_types,
    }
    return direct_to_template(request, "profile/userprofile_policylist.html", extra_context)

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

