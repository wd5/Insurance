from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from profile.forms import ProfileForm, PersonaForm
from profile.models import UserProfile,Persona
from calc.models import InsurancePolicy
import copy

from django.views.generic.list_detail import object_list



@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    # Process delete form
    persona_post_flag = False
    if request.method == 'POST' and request.POST.has_key('delete_flag'):
        persona_post_flag = True
        if request.POST['action_type'] == 'ask':
            persona_obj = Persona.objects.get(id=request.POST['persona_id'])
            return render_to_response('profile/userprofile_edit_delete_ask.html', {
                    'persona':persona_obj,
                    }, context_instance=RequestContext(request))
        if request.POST['action_type'] == 'delete':
            persona = Persona.objects.get(id=request.POST['persona_id'])
            persona.delete()

    # Process persona forms
    if request.method == 'POST' and request.POST.has_key('persona_flag'):
        persona_post_flag = True
        if request.POST.has_key('persona_id'):
            persona_id = int(request.POST['persona_id'])
            instance = Persona.objects.get(pk=persona_id)
            persona_form = PersonaForm(request.POST,instance=instance)
            if persona_form.is_valid():
                persona_form.save()
        else:
            new = Persona()
            new.first_name = request.POST['first_name']
            new.last_name = request.POST['last_name']
            new.middle_name = request.POST['middle_name']
            new.me = False
            new.user = user
            new.save()
    persona_me = Persona.objects.get(user=user,me=True)
    persona = Persona.objects.filter(user = user,me=False)

    persona_forms = []
    # For the first row
    persona_forms.append(PersonaForm(instance=persona_me))
    for p in persona:
        persona_forms.append(PersonaForm(instance=p))
    # For the last empty row
    persona_forms.append(PersonaForm())

    saved=False
    if request.method == 'POST' and (not persona_post_flag): 
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            saved = True
    else:
        profile_form = ProfileForm(instance=profile)

    return render_to_response('profile/userprofile_edit.html', {
        'profile_form': profile_form,
        'saved': saved,
        'persona':persona,
        'persona_me':persona_me,
        'persona_forms':persona_forms,
    }, context_instance=RequestContext(request))


@login_required
def policy_list(request, policy_type=None):
    policy_types = dict(InsurancePolicy.TYPE_CHOICES)
    if not policy_type:
        policy_type, _ = InsurancePolicy.TYPE_CHOICES[0]
    user = request.user
    query = InsurancePolicy.objects.filter(user=user, type=policy_type)
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
