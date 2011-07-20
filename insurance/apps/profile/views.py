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
    print "========================================"
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    persona_post_flag = False

    # Process persona forms
    if request.method == 'POST' and request.POST.has_key('persona_flag'):
        persona_post_flag = True
        print '-------------------- PERSONA FLAG --------------------'
        for k,v in request.POST.items():
            print "%-20s%-20s" % (k,v)
        if request.POST.has_key('persona_id'):
            persona_id = int(request.POST['persona_id'])
            print "persona_id =", persona_id
            instance = Persona.objects.get(pk=persona_id)
            persona_form = PersonaForm(request.POST,instance=instance)
            if persona_form.is_valid():
                print "IS VALID"
                persona_form.save()
            else:
                print "IS NOT VALID"
                print persona_form.errors
        else:
            new = Persona()
            new.first_name = request.POST['first_name']
            new.last_name = request.POST['last_name']
            new.middle_name = request.POST['middle_name']
            new.me = False
            new.user = user
            new.save()
            print "PERSONA_ID NO"
        

    persona_me = Persona.objects.get(user=user,me=True)
    persona = Persona.objects.filter(user = user,me=False)

    persona_forms = []
    # For the first row
    persona_forms.append(PersonaForm(instance=persona_me))
    i = 0
    print i,"*", persona_me.id, persona_me.last_name, persona_me.me
    i += 1
    for p in persona:
        print i," ",p.id,p.last_name,p.me
        persona_forms.append(PersonaForm(instance=p))
        i += 1
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
def policy_list(request):
    user = request.user
    query = InsurancePolicy.objects.filter(user=user)
    context = {
        "template_name": "profile/userprofile_policylist.html",
        "queryset": query,
        "template_object_name": "policy"
    }
    return object_list(request, **context)
