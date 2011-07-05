from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from profile.forms import ProfileForm
from profile.models import UserProfile



@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST': 
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=profile)

    return render_to_response('profile/userprofile_edit.html', {
        'form': form,
    }, context_instance=RequestContext(request))
