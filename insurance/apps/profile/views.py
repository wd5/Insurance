from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from profile.forms import ProfileForm, PersonaForm
from profile.models import UserProfile,Persona
from calc.models import InsurancePolicy

from django.views.generic.list_detail import object_list



@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    saved=False
    if request.method == 'POST': 
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save()
            saved = True
    else:
        profile_form = ProfileForm(instance=profile)

    persona_me = Persona.objects.get(user=user, me=True)
    personas = Persona.objects.filter(user=user, me=False)

    return render_to_response('profile/userprofile_edit.html', {
        'profile_form': profile_form,
        'saved': saved,
        'personas': personas,
        'persona_me': persona_me,
    }, context_instance=RequestContext(request))

@login_required
def edit_persona(request, persona_id=None):
    user = request.user
    if persona_id:
        persona = get_object_or_404(Persona, pk=persona_id)
        if request.method == 'POST': 
            persona_form = PersonaForm(request.POST, instance=persona)
            if persona_form.is_valid():
                persona_form.save()
        else:
            persona_form = PersonaForm(instance=persona)
    else:
        if request.method == 'POST': 
            persona_form = PersonaForm(request.POST)
            if persona_form.is_valid():
                persona = persona_form.save(commit=False)
                persona.user = user
                persona.save()
                return HttpResponseRedirect(reverse('userprofile_edit'))
        else:
            persona_form = PersonaForm()
    return render_to_response('profile/userprofile_addpersona.html', {
        'persona_form': persona_form,
    }, context_instance=RequestContext(request))

@login_required
def delete_persona(request, persona_id):
    # TODO: Removal confirmation 
    persona = get_object_or_404(Persona, pk=persona_id)
    persona.delete()
    return HttpResponseRedirect(reverse('userprofile_edit'))


@login_required
def policy_list(request, policy_type=None):
    policy_types = dict(InsurancePolicy.TYPE_CHOICES)
    if not policy_type:
        policy_type, _ = InsurancePolicy.TYPE_CHOICES[0]
    user = request.user
    personas = user.persona_set.all()
    # TODO: i wonder if the whole "in" thing works :)
    query = InsurancePolicy.objects.filter(persona__in=personas, type=policy_type)
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
