from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from profile.forms import ProfileForm
from profile.forms import UserForm
from profile.models import UserProfile



@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST': 
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render_to_response('profile/userprofile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    }, context_instance=RequestContext(request))
