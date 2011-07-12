from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from profile.forms import ProfileForm
from profile.models import UserProfile
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
            profile_form.save()
            saved = True
    else:
        profile_form = ProfileForm(instance=profile)

    return render_to_response('profile/userprofile_edit.html', {
        'profile_form': profile_form,
        'saved': saved
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
